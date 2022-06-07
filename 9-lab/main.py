import cv2
import numpy as np


VIDEO = 'videos/Cars_On_Highway_short.mp4'
CLASSES = 'model/coco.names'
MODEL_CONF = 'model/yolov3-320.cfg'
MODEL_WEIGHTS = 'model/yolov3-320.weights'


class VehiclesRecognition:
  def __init__(self,
    video_name,
    classes_file,
    model_conf,
    model_weights,
    blob_size,
    conf_threshold,
    nms_threshold,
    classes_idx_required,
  ):
    self.__video = cv2.VideoCapture(video_name)
    self.__classes = open(classes_file).read().strip().split('\n')
    self.__classes_idx_required = classes_idx_required
    self.__blob_size = blob_size
    self.__conf_threshold = conf_threshold
    self.__nms_threshold = nms_threshold
    np.random.seed(42)
    self.__colors = np.random.randint(0, 255, size=(len(self.__classes), 3), dtype='uint8')
    self.__net = cv2.dnn.readNetFromDarknet(model_conf, model_weights)
    self.__net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    self.__net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)


  def operate_frames(self, label='Vehicles recognition'):
    while True:
      if cv2.waitKey(1) == ord('q'): break
      success, img = self.__video.read()
      if not success or img is None: break

      img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
      # channels division
      blue_chan = img.copy()
      blue_chan[:,:,1:] = 0
      red_chan = img.copy()
      red_chan[:,:,:-1] = 0
      c1, c2 = tuple(self.__channel_recognition(chan) for chan in (blue_chan, red_chan))
      containers = list()
      for i in range(len(c1)):
        containers.append(c1[i] + c2[i])
      self.__show_found_objects(img, containers)
      cv2.imshow(label, img)

    self.__video.release()
    cv2.destroyAllWindows()


  def __channel_recognition(self, img):
    input_size = (self.__blob_size, self.__blob_size)
    blob = cv2.dnn.blobFromImage(img, 1 / 255, input_size, [0, 0, 0], 1, crop=False)
    # Set the input of the network
    self.__net.setInput(blob)
    layer_names = self.__net.getLayerNames()
    out_layers = self.__net.getUnconnectedOutLayers()
    outputNames = [layer_names[i - 1] for i in out_layers]
    
    # Feed data to the network
    outputs = self.__net.forward(outputNames)
    # Find the objects from the network output
    return self.__search_objects(outputs, img)
  

  def __search_objects(self, outputs, img):
    height, width = img.shape[:2]
    boxes = list()
    class_ids = list()
    confidence_scores = list()

    for output in outputs:
      for det in output:
        scores = det[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if class_id not in self.__classes_idx_required: continue
        if confidence <= self.__conf_threshold: continue
        w = int(det[2] * width)
        h = int(det[3] * height)
        x = int((det[0] * width) - w / 2)
        y = int((det[1] * height) - h / 2)
        boxes.append([x, y, w, h])
        class_ids.append(class_id)
        confidence_scores.append(float(confidence))

    return boxes, class_ids, confidence_scores


  def __show_found_objects(self, img, containers):
    boxes, class_ids, confidence_scores = containers
    # Apply Non-Max Suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidence_scores, self.__conf_threshold, self.__nms_threshold)
    for i in indices.flatten():
      x, y, w, h = boxes[i][:4]
      color = [int(c) for c in self.__colors[class_ids[i]]]
      name = self.__classes[class_ids[i]]
      # Draw classname and confidence score 
      text = '{} {}%'.format(name.upper(), int(confidence_scores[i] * 100))
      cv2.putText(img, text,(x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
      cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)


if __name__ == '__main__':
  vh = VehiclesRecognition(
    video_name=VIDEO,
    classes_file=CLASSES,
    model_conf=MODEL_CONF,
    model_weights=MODEL_WEIGHTS,
    blob_size=320,
    conf_threshold=0.2,
    nms_threshold=0.2,
    classes_idx_required=[2, 3, 5, 7]
  )

  vh.operate_frames()
