S3 Lab Dataset (Ready to Upload)
--------------------------------
This folder contains a complete dummy dataset for your Amazon S3 lab.

Notes:
- PDF files are valid, multi-page PDFs.
- CSV and TXT files contain sample data.
- lecture.mp4 files are minimal placeholders intended only for S3 CRUD tests.
  If you need a playable video, upload any small 10–30s MP4 and overwrite the placeholder.
- Includes an extra 'temp.csv' under datasets/CS101 to use for the 'delete' task.

Suggested S3 Layout:
- Enable bucket versioning BEFORE uploads.
- Upload the folders as-is to your bucket.
- Use presigned URLs for slides.pdf and a submission PDF per your lab.

Folder Tree:
announcements/
courses/
datasets/
submissions/
  2025-09-25.txt
  2025-10-05.txt
  CS101/
  CS202/
    marks.csv
    temp.csv
    attendance.csv
  CS101/
  CS202/
    weeks/
      week01/
      week02/
        lecture.mp4
        slides.pdf
        slides.pdf
    weeks/
      week01/
      week02/
        lecture.mp4
        slides.pdf
        slides.pdf
  CS101/
  CS202/
    assignment1/
      2023001/
      2023002/
        assignment.pdf
        assignment.pdf
    assignment1/
      2023010/
      2023011/
        assignment.pdf
        assignment.pdf