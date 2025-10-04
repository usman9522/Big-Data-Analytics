# AWS S3 Object Storage Lab 🪣☁️

A comprehensive Python-based project demonstrating AWS S3 (Simple Storage Service) operations including file uploads, downloads, bucket management, and presigned URL generation.

## 📋 Table of Contents
- [About the Project](#about-the-project)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [AWS IAM Permissions](#aws-iam-permissions)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Security Best Practices](#security-best-practices)
- [Author](#author)

## 🎯 About the Project

This project is part of the **Big Data Analytics Lab Assignment** focusing on AWS S3 Object Storage. It provides a command-line interface (CLI) for performing various S3 operations using Python's `boto3` library.

### What is AWS S3?
Amazon S3 (Simple Storage Service) is a scalable object storage service that offers:
- 99.999999999% (11 9's) durability
- Virtually unlimited storage
- High availability and performance
- Security and compliance features

## ✨ Features

The application provides an interactive menu with the following capabilities:

| Feature | Description |
|---------|-------------|
| 🗂️ **List All Buckets** | View all S3 buckets in your AWS account |
| 📂 **List All Objects** | Display all files in a specific bucket |
| 📁 **List Folder Objects** | View files in a specific folder/prefix |
| ⬆️ **Upload File** | Upload individual files with custom S3 paths |
| 📤 **Upload Directory** | Upload entire folders maintaining directory structure |
| ⬇️ **Download File** | Download files from S3 to local machine |
| 🗑️ **Delete Object** | Remove files from S3 bucket |
| 🔗 **Generate Presigned URL** | Create temporary shareable links (with expiration) |
| 📋 **Copy Object** | Copy files within S3 |
| 🆕 **Create Bucket** | Create new S3 buckets |
| ❌ **Delete Bucket** | Remove buckets and all their contents |

## 🔧 Prerequisites

- Python 3.7 or higher
- AWS Account with IAM user credentials
- Basic knowledge of AWS S3
- Command-line interface (PowerShell/Terminal)

## 📥 Installation

### 1. Clone the Repository

```powershell
git clone https://github.com/usman9522/Big-Data-Analytics.git
cd Big-Data-Analytics/lab02
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

**Dependencies:**
- `boto3` - AWS SDK for Python
- `python-dotenv` - Load environment variables from .env file

## ⚙️ Configuration

### 1. Create `.env` File

Copy the example file and add your credentials:

```powershell
cp .env.example .env
```

### 2. Add AWS Credentials

Edit the `.env` file with your actual AWS credentials:

```env
# AWS Credentials
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_access_key_here
AWS_DEFAULT_REGION=us-east-2

# S3 Bucket Name (Optional)
BUCKET_NAME=your-bucket-name
```

### 3. Getting AWS Credentials

1. **Log in to AWS Console**: https://console.aws.amazon.com/
2. Navigate to **IAM** (Identity and Access Management)
3. Click on **Users** → Your username
4. Go to **Security credentials** tab
5. Click **Create access key**
6. Select **Command Line Interface (CLI)**
7. Copy the **Access Key ID** and **Secret Access Key**
8. Paste them into your `.env` file

**⚠️ IMPORTANT:** Never commit the `.env` file to Git! It's already in `.gitignore`.

## 🚀 Usage

### Running the Application

```powershell
python main.py
```

### Interactive Menu

After running, you'll see:

```
==================================================
AWS S3 Operations Demo
==================================================

Fetching your available buckets...

=== Available S3 Buckets ===
  - bucket-1 (Created: 2025-10-01 10:30:00+00:00)
  - bucket-2 (Created: 2025-10-02 15:45:00+00:00)

Enter your S3 bucket name: your-bucket-name

==================================================
Choose an operation:
1. List all buckets
2. List all objects in bucket
3. List objects in a specific folder
4. Upload a file
5. Download a file
6. Delete an object
7. Upload a directory
8. Generate presigned URL
9. Copy an object
10. Create a new bucket
11. Delete a bucket
0. Exit
==================================================
```

## 📁 Project Structure

```
lab02/
│
├── main.py                    # Main Python script with S3 operations
├── .env                       # Environment variables (DO NOT COMMIT)
├── .env.example              # Template for environment variables
├── .gitignore                # Git ignore patterns
├── requirements.txt          # Python dependencies
├── README.md                 # This documentation file
├── Lab Assignment s3.pdf     # Assignment instructions
│
├── s3_lab_dataset/           # Sample dataset for uploading
│   └── s3_lab_dataset/
│       ├── README.txt
│       ├── announcements/    # Announcement files
│       ├── courses/          # Course materials (videos, PDFs)
│       ├── datasets/         # CSV data files
│       └── submissions/      # Student submissions
│
└── ss/                       # Screenshots of S3 operations
```

## 🔐 AWS IAM Permissions

Your IAM user needs the following S3 permissions:

### Option 1: Full S3 Access (Easiest)
Attach the **AmazonS3FullAccess** managed policy.

### Option 2: Custom Policy (More Secure)

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetBucketLocation",
                "s3:ListAllMyBuckets"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:PutObjectAcl"
            ],
            "Resource": "arn:aws:s3:::your-bucket-name/*"
        }
    ]
}
```

## 💡 Examples

### Example 1: Upload a File to Specific Folder

```
Choose operation: 4
Enter file path: E:\path\to\file.pdf
Enter S3 object name: courses/CS101/weeks/week01/slides.pdf
```

Result: File uploaded to `s3://bucket-name/courses/CS101/weeks/week01/slides.pdf`

### Example 2: Upload Entire Directory

```
Choose operation: 7
Enter directory path: E:\path\to\s3_lab_dataset
Enter S3 prefix: 
```

Result: All files uploaded maintaining folder structure

### Example 3: Generate Presigned URL

```
Choose operation: 8
Enter object name: courses/CS101/weeks/week01/slides.pdf
Enter expiration (seconds): 3600
```

Result: Shareable URL valid for 1 hour

### Example 4: List Specific Folder

```
Choose operation: 3
Enter folder path: courses/CS101/
```

Result: Lists all files in the CS101 course folder

## 🐛 Troubleshooting

### Error: "NoCredentialsError"
**Cause:** AWS credentials not found  
**Solution:** Check your `.env` file has correct `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`

### Error: "403 Forbidden"
**Cause:** Insufficient permissions  
**Solution:** Add `AmazonS3FullAccess` policy to your IAM user

### Error: "NoSuchBucket"
**Cause:** Bucket name doesn't exist or typo  
**Solution:** Verify bucket name matches exactly (case-sensitive)

### Error: "InvalidRequest - Authorization mechanism not supported"
**Cause:** Wrong AWS region configuration  
**Solution:** Update `AWS_DEFAULT_REGION` in `.env` to match your bucket's region

### Error: "PermissionError: [Errno 13]"
**Cause:** Trying to upload a directory as a file  
**Solution:** Use option 7 (Upload Directory) for folders, option 4 for individual files

### Error: "BucketAlreadyExists"
**Cause:** Bucket name is already taken globally  
**Solution:** S3 bucket names must be globally unique. Try a different name

## 🔒 Security Best Practices

- ✅ **Never commit** `.env` file to version control
- ✅ **Use environment variables** for sensitive data
- ✅ **Apply principle of least privilege** - only grant necessary IAM permissions
- ✅ **Rotate access keys** regularly (every 90 days recommended)
- ✅ **Enable MFA** (Multi-Factor Authentication) on your AWS account
- ✅ **Monitor AWS CloudTrail** logs for suspicious activity
- ✅ **Use IAM roles** instead of access keys when possible
- ✅ **Set expiration times** on presigned URLs (default: 1 hour)

## 📚 AWS S3 Key Concepts

### Bucket
- A container for objects stored in S3
- Globally unique name
- Region-specific

### Object
- Files stored in S3 buckets
- Consists of data and metadata
- Identified by a unique key (path)

### Prefix/Folder
- Logical grouping using forward slashes in object keys
- Example: `courses/CS101/week01/slides.pdf`

### Presigned URL
- Temporary URL for accessing private S3 objects
- Time-limited access
- No AWS credentials required for the recipient

## 🎓 Learning Outcomes

Through this lab, you will learn:
- How to interact with AWS S3 using Python SDK (boto3)
- Object storage concepts and operations
- AWS IAM permissions and security
- Environment variable management
- Error handling in cloud applications
- CLI application development

## 👨‍💻 Author

**Usman**
- GitHub: [@usman9522](https://github.com/usman9522)
- Repository: [Big-Data-Analytics](https://github.com/usman9522/Big-Data-Analytics)
- Course: Big Data Analytics (Semester 7)
- Lab: AWS S3 Object Storage

## 📄 License

This project is for educational purposes as part of university coursework.

## 🤝 Contributing

This is an academic project, but suggestions and improvements are welcome!

## 📞 Support

For questions or issues:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review AWS S3 documentation
3. Check boto3 documentation

---

**⭐ If you found this helpful, please star the repository!**

**📌 Note:** This project demonstrates AWS S3 operations for educational purposes. Always follow AWS best practices and security guidelines in production environments.
