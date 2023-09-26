# PLAN

taken from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5146644/


1.
Approach one: A large set of image features that may, or may not, have a meaningful radiological interpretation are automatically computed. The computed features are used only as intermediate quantities by an algorithm to produce a final binary-valued label describing the class of the nodule (e.g., as malignant or benign). Such features could be calculated, e.g., by the hidden layers of a neural network or by a wavelet transform.<br>
2.
Approach two: Diagnostic image features from various medical–radiological terminology sets are specifically computed and quantified algorithmically. For development of the algorithms, these quantified feature values are validated against the quantifications of the same diagnostic image features made by radiologists. Obtaining quantified diagnostic image features may be the end goal (for the purpose of displaying them to the radiologist for consideration during nodule assessment) or may be used instead (or additionally) as inputs to a larger CAD system to automatically classify the nodule (e.g., as malignant or benign).
