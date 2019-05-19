import numpy as np

from deep_sort import preprocessing
from deep_sort import nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from deep_sort.detection import Detection as ddet

import generate_detections as gdet


class tracker:
    def __init__(self):
        # Definition of the parameters
        max_cosine_distance = 0.3
        nn_budget = None
        self.nms_max_overlap = 1.0
        # deep_sort 
        model_filename = 'model_data/mars-small128.pb'
        self.encoder = gdet.create_box_encoder(model_filename,batch_size=1)
        metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
        self.tracker = Tracker(metric)
        self.trackedIDs = {}
        self.tracedIDtoLabels = {}

    def track(self, frame, dknetBoxs):
        boxs = [list(i[2]) for i in dknetBoxs]
        labels = [i for i in dknetBoxs]
        features = self.encoder(frame,boxs)
        detections = [Detection(bbox, 1.0, feature) for bbox, feature in zip(boxs, features)]    
        # Run non-maxima suppression.
        boxes = np.array([d.tlwh for d in detections])
        scores = np.array([d.confidence for d in detections])
        indices = preprocessing.non_max_suppression(boxes, self.nms_max_overlap, scores)
        detections = [detections[i] for i in indices]
        print("Detections: ", detections)
        # Call the traccker
        self.tracker.predict()
        self.tracker.update(detections, labels)
        retVal = []
        for track in self.tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue 
            bbox = track.to_tlbr()
            if track.track_id not in self.trackedIDs:
                self.trackedIDs[ track.track_id ] = 1
                
                retVal.append( track.label )
        return retVal

