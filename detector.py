import json
import numpy as np
import cv2
from utils import toRGB, rotation_angle, get_distance_to_object

with open("config.json") as file:
    config = json.load(file)
    yolo_config = config["yolo_config"]

X_CENTER = 1920 // 2
Y_CENTER = 1080 // 2


class Detector:
    def __init__(self):
        self.colors = [(0, 0, 255), (255, 0, 0)]
        self.labels = open(yolo_config["names"]).read().strip().split("\n")
        self.min_confidence = yolo_config["min_confidence"]
        self.threshold = yolo_config["threshold"]
        self.weights_path = yolo_config["weights"]
        self.cfg_path = yolo_config["network_cfg"]
        self.input_img_size = yolo_config["input_size"]
        # Se cargan yolo con los pesos usando OpenCV
        self.yolo_detector = cv2.dnn.readNetFromDarknet(
            self.cfg_path, self.weights_path
        )
        self.output_layers = self.__get_output_layers()

    def detect(self, image):
        H, W = image.shape[:2]
        boxes = []
        confidences = []
        classIDS = []
        blob = cv2.dnn.blobFromImage(
            image,
            1 / 255.0,
            (self.input_img_size[0], self.input_img_size[1]),
            swapRB=True,
            crop=False,
        )
        self.yolo_detector.setInput(blob)
        outputs = self.yolo_detector.forward(self.output_layers)
        # Iteracion sobre las salidas de la red
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                # Se filtran las malas predicciones
                if confidence > self.min_confidence:
                    box = detection[0:4] * np.array([W, H, W, H])
                    centerX, centerY, width, height = box.astype(int)
                    # Calculo de la esquina superior izquierda del bbox
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDS.append(classID)

        # Se eliminan los bbox malos
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.min_confidence, self.threshold)
        result, ang, dists = self.__get_angles_and_distances(idxs, boxes, classIDS)
        # Diccionario con la imagen, distancia y angulo de rotacion por cada clase encontrada
        return {
            "ploted_img": self.__plot_results(image, idxs, boxes, confidences, classIDS, ang, dists),
            "location_data": result
        }
        
    def __get_angles_and_distances(self, idxs, boxes, classIDS):
        angles = []
        distances = []
        results = {}
        if len(idxs) > 0:
            for i in idxs.flatten():
                x, y = boxes[i][0], boxes[i][1]
                w, h = boxes[i][2], boxes[i][3]
                x_center = x + w // 2
                y_center = y + h // 2
                class_ = self.labels[classIDS[i]]
                # Estos calculos solo funcionan con la configuración para la camara de mi telefono
                # para usar otra camara hay que cambiar los parametros camera_calibration del archivo config.json
                rot_angle = rotation_angle(
                    class_, (x_center, y_center), (X_CENTER, Y_CENTER)
                )
                # w = w // w
                distance = get_distance_to_object(class_, w)
                angles.append(rot_angle)
                distances.append(distance)
                results[class_] = {"distance": distance, "rot_angle": rot_angle}
        return results, angles, distances

    def __plot_results(self, image, idxs, boxes, confidences, classIDS, angles, distances):
        # Grafica los resultados
        if len(idxs) > 0:
            for i in idxs.flatten():
                x, y = boxes[i][0], boxes[i][1]
                w, h = boxes[i][2], boxes[i][3]
                color = [int(c) for c in self.colors[classIDS[i]]]
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 8)
                #text = "{}: {:.4f} cm".format(self.labels[classIDS[i]], distances[i - 1])
                #text = "{}: {:.4f}".format(self.labels[classIDS[i]], angles[i - 1])
                text = "{}: {:.4f}".format(self.labels[classIDS[i]], confidences[i])
                cv2.putText(
                    image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 2.5, color, 2
                )
        return toRGB(image)

    def __get_output_layers(self):
        ln = self.yolo_detector.getLayerNames()
        return [ln[i[0] - 1] for i in self.yolo_detector.getUnconnectedOutLayers()]
