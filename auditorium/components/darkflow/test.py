from net.build import TFNet
import cv2

options = {"model": "cfg/yolo.cfg", "load": "bin/yolo.weights"}

tfnet = TFNet(options)

imgcv = cv2.imread("/Users/ruslan/0_persons.jpg")
result = tfnet.return_predict(imgcv)
print("Original: {}".format(0))
print("Persons: {}".format(len([x["label"] for x in result if x["label"] == "person"])))

imgcv = cv2.imread("/Users/ruslan/7_persons.jpg")
result = tfnet.return_predict(imgcv)
print("Original: {}".format(7))
print("Persons: {}".format(len([x["label"] for x in result if x["label"] == "person"])))

for finding in result:
    if finding["label"] == "person":
        cv2.rectangle(imgcv,
                   (finding["topleft"]["x"], finding["topleft"]["y"]),
                   (finding["bottomright"]["x"], finding["bottomright"]["y"]),
                   (255,0,0),
                   2)

cv2.imwrite("/Users/ruslan/7_persons_findings.jpg", imgcv)

imgcv = cv2.imread("/Users/ruslan/11_persons.jpg")
result = tfnet.return_predict(imgcv)
print("Original: {}".format(11))
print("Persons: {}".format(len([x["label"] for x in result if x["label"] == "person"])))

for finding in result:
    if finding["label"] == "person":
        cv2.rectangle(imgcv,
                   (finding["topleft"]["x"], finding["topleft"]["y"]),
                   (finding["bottomright"]["x"], finding["bottomright"]["y"]),
                   (255,0,0),
                   2)

cv2.imwrite("/Users/ruslan/11_persons_findings.jpg", imgcv)

imgcv = cv2.imread("/Users/ruslan/12_persons.jpg")
result = tfnet.return_predict(imgcv)
print("Original: {}".format(12))
print("Persons: {}".format(len([x["label"] for x in result if x["label"] == "person"])))

for finding in result:
    if finding["label"] == "person":
        cv2.rectangle(imgcv,
                   (finding["topleft"]["x"], finding["topleft"]["y"]),
                   (finding["bottomright"]["x"], finding["bottomright"]["y"]),
                   (255,0,0),
                   2)

cv2.imwrite("/Users/ruslan/12_persons_findings.jpg", imgcv)

imgcv = cv2.imread("/Users/ruslan/13_persons.jpg")
result = tfnet.return_predict(imgcv)
print("Original: {}".format(13))
print("Persons: {}".format(len([x["label"] for x in result if x["label"] == "person"])))

for finding in result:
    if finding["label"] == "person":
        cv2.rectangle(imgcv,
                   (finding["topleft"]["x"], finding["topleft"]["y"]),
                   (finding["bottomright"]["x"], finding["bottomright"]["y"]),
                   (255,0,0),
                   2)

cv2.imwrite("/Users/ruslan/13_persons_findings.jpg", imgcv)
