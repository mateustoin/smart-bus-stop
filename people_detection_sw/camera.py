import cv2
import numpy as np
from threading import Thread, Lock
from time import sleep
import os

global people_count
people_count = 0

lock = Lock()


# /tmp/people_counter
def escrever_numero_no_arquivo(nome_arquivo):
    while True:
        with open(nome_arquivo, "w") as arquivo:
            try:
                lock.acquire()
                arquivo.seek(0)
                arquivo.truncate()
                counter = str(people_count)
                arquivo.write(counter)
                arquivo.flush()  # Força a escrita imediata no arquivo
                os.fsync(
                    arquivo.fileno()
                )  # Garante a sincronização com o sistema operacional
            finally:
                lock.release()
            sleep(30)  # Define o tempo de atualização


# Carrega o modelo YOLO (considere usar yolov3-tiny para melhor performance)
net = cv2.dnn.readNet("./yolov4-tiny.weights", "./yolov4-tiny.cfg")

# Captura de vídeo da webcam
cap = cv2.VideoCapture(0)

# Verifica se a webcam foi aberta corretamente
if not cap.isOpened():
    print("Erro: Não foi possível abrir a webcam.")
    exit()

layer_names = net.getLayerNames()
output_layer_names = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

written_thread = Thread(target=escrever_numero_no_arquivo, args=["/tmp/people_counter"])


try:
    written_thread.start()
    # written_thread.join()
    while True:
        # Lê o frame da webcam
        ret, frame = cap.read()

        if not ret:
            print("Erro: Não foi possível ler o frame.")
            break

        # Redimensiona o frame para um tamanho menor para detecção mais rápida
        (height, width) = frame.shape[:2]
        resized_frame = cv2.resize(frame, (320, 320))

        # Define a entrada da rede neural
        blob = cv2.dnn.blobFromImage(
            resized_frame, 1 / 255.0, (320, 320), swapRB=True, crop=False
        )
        net.setInput(blob)

        # Realiza a propagação para a frente
        outputs = net.forward(output_layer_names)

        # Inicializa as listas para caixas detectadas, confidências e IDs de classe
        boxes = []
        confidences = []
        class_ids = []

        # Loop sobre as camadas de saída
        for output in outputs:
            # Loop sobre as detecções
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                # Considera apenas a classe 'pessoa' e detecções com alta confiança
                if class_id == 0 and confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Coordenadas do retângulo
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    # Adiciona às listas
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # Aplica a Supressão Não Máxima para eliminar caixas redundantes
        indices = cv2.dnn.NMSBoxes(
            boxes, confidences, score_threshold=0.5, nms_threshold=0.4
        )

        # Conta o número de pessoas detectadas após NMS
        lock.acquire()
        people_count = len(indices)
        lock.release()

        # Exibe a contagem de pessoas no terminal
        print(f"Número de pessoas detectadas: {people_count}")

        # Se desejar adicionar uma condição de saída, por exemplo, após um certo tempo ou ao pressionar uma tecla
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except KeyboardInterrupt:
    # Permite interromper o loop com Ctrl+C
    pass

# Libera a webcam e fecha todas as janelas
cap.release()
cv2.destroyAllWindows()
