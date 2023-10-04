import cv2

class Tracker:
    def __init__(self):
        self.tracker = cv2.TrackerCSRT_create()
        self.video_path = None
        self.bbox = None
        self.video = None

    def load_video(self):
        self.video = cv2.VideoCapture(self.video_path)

    def select_roi(self):
        ok, frame = self.video.read()
        if not ok:
            print("Erro ao carregar o vídeo.")
            return False

        bbox = cv2.selectROI(frame)
        self.bbox = bbox
        return True

    def start_tracking(self):
        if self.video is None:
            print("Carregue o vídeo antes de iniciar o rastreamento.")
            return

        ok, frame = self.video.read()
        if not ok:
            print("Erro ao ler o próximo quadro do vídeo.")
            return

        ok = self.tracker.init(frame, self.bbox)

        while True:
            ok, frame = self.video.read()
            if not ok:
                break

            ok, bbox = self.tracker.update(frame)

            if ok:
                (x, y, w, h) = [int(v) for v in bbox]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3, 1)
            else:
                cv2.putText(frame, 'Falha no Rastreamento', (100, 80), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 255), 2)

            cv2.imshow('Rastreando', frame)

            if cv2.waitKey(1) & 0XFF == 27:
                break

if __name__ == "__main__":
    tracker = Tracker()
    tracker.video_path = input("Digite o caminho do arquivo de vídeo: ")
    
    if tracker.video_path:
        tracker.load_video()
        print("Selecione a região de interesse (ROI) com o mouse.")
        if tracker.select_roi():
            tracker.start_tracking()
