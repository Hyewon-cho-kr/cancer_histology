import cv2
import glob, os
import numpy as np
from tqdm import tqdm

class area_filter():
    
    def __init__(self, tissue_dir, staining_th, area_th): # directories with 'tissue' || ScanAreas as subdirectories
        self.tissue_dir = tissue_dir
        self.staining_th = staining_th
        self.area_th = area_th
    
    def _get_tissue_area(self, img_dir):
    
        img_gray = cv2.imread(img_dir, 0)
        _, thr = cv2.threshold(img_gray, self.staining_th, 255, cv2.THRESH_BINARY_INV)
        
        tissue_area = int(np.sum(thr/255))
        total_area = img_gray.shape[0] * img_gray.shape[1]
        
        self.ratio = tissue_area / total_area

    
    def get_outarea_index(self, areas):
        out_index = []

        for area in tqdm(areas) :
            area_exclusion = []
            area_exclusion.append(area)
            test_scan = sorted(glob.glob(os.path.join(area, '**.jpg')))
            for idx, scans in enumerate(test_scan):
                tissue_ratio = self._get_tissue_area(scans)
                if self.ratio < self.area_th:
                    area_exclusion.append(idx)
            out_index.append(area_exclusion)
        
        return out_index
    
    def main(self):
        
        tissue_areas = sorted(glob.glob(os.path.join(self.tissue_dir, 'ScanArea**')))
        tissue_ratio = self.get_outarea_index(tissue_areas)
        
        return tissue_ratio