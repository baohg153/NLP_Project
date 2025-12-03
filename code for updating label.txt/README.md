# As observed, PPOCRLabel is pretty bad at OCR-ing Vietnamese images, with plenty of spelling mistakes. This code is designed to help correcting spelling mistakes inthe  Label.txt file - created from PPOCRLabel, with a spelling-correct text file created from VietOCR (or any good Vietnamese OCR tools).

# Special library used: fuzzywuzzy
- pip install fuzzywuzzy

# Instructions
1. First, use PPOCRLabel and export `Label.txt` file, then put it in this source code folder.
2. Then, download VietOCR to re-OCR the images (with the link download below). VietOCR can convert images to a text file with a quite high spelling accuracy and correct line breaks.
    - Downloading VietOCR at: https://sourceforge.net/projects/vietocr/
3. Use VietOCR to OCR images and export the output textfile to this folder, with the name `correct_text.txt`.
4. In `utils.ipynb`, run the code to remove all empty lines in `correct_text.txt`.
5. Then, run the `main.py` to get `NewLabel.txt` as new Label.txt file.
6. At this time, you've got new Label.txt, which is good. Now, to update the `rec_gt.txt` file (which is exported from PPOCRLabl) according to `NewLabel.txt`, do the following steps:
    - Move the `NewLabel.txt` file to the dataset folder, and change its name to `Label.txt`.
    - Open PPOCRLabel and open the dataset folder.
    - File -> Export Recognition Result
Following the 6 steps above, then you've done updating `Label.txt` and `rec_gt.txt`.

# Notes
- For some reasons, the first line (in the first page) may be updated incorrectly, so you should check it manually.
- This process does not guarantee all spellings are correct, as it depends on the OCR quality of VietOCR (or the other OCR tools that you use). However, it is certain that the quality has been much better compared to the original PPOCRLabl.