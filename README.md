# Custom Python HTTP Web Server (Homework)

## 📝 Project Overview

This project implements a basic single-threaded HTTP/1.1 web server from the ground up using Python's low-level **`socket`** library. It fulfills the assignment requirements by manually handling connection establishment, raw request reading, HTTP parsing, file serving, and connection closure.

### 📌 Core Scope and Limitations

* **Supported Method:** `GET` only.
* **Supported Protocol:** HTTP/1.0 and HTTP/1.1 requests are processed to serve static files.
* **Unsupported Features:** Redirects, persistent connections (Keep-Alive), `POST`, `HEAD`, or other HTTP methods are **not** supported and are outside the scope of this assignment.

## 🚀 How to Run the Server and Testing Procedure

### Prerequisites

* You must have **Python 3.x** installed on your system.
* The server script (`server.py`) and all requested files must be in the same working directory.

### Running the Server

1.  **Preparation (Testing Environment):** The testing environment will involve unzipping a `testfiles.zip` file, creating a `testfiles` folder, and copying `server.py` into it. **All requested files will reside in this working directory.**

2.  **Launch:** Navigate to the folder containing `server.py` and run the server:
    ```bash
    python server.py
    ```

3.  **Access:** The server will start listening on the configured host and port.
    > **Default URL:** `http://127.0.0.1:8080`

4.  **Stop:** Use **`Ctrl+C`** in the terminal to stop the server.

---

## 🧪 Testing and Validation

The server will be validated using both automated file comparisons and visual browser tests.

### 1. File Integrity and Error Testing (10 Test Cases)

The server's response will be compared against the original files to ensure data integrity.

| Test Case | Description | Expected Outcome | Teammate Focus |
| :--- | :--- | :--- | :--- |
| **9 x Static Files** | Requesting various files from the `testfiles` folder (e.g., text, images). | Server returns the content of the requested file byte-for-byte. | Teammate 2 (File I/O) |
| **1 x Non-Existent File** | Requesting a file that does not exist in the directory. | Server returns a **`404 Not Found`** status code and a corresponding error page body. | Teammate 2 (Error Handling) |

### 2. Visual Browser Test (Critical Requirement)

The server will be run on various hosts and accessed by at least two different browsers (e.g., Chrome, Firefox).

* **Success Condition:** All files, especially images, CSS, and HTML, must render **correctly** in the browser.
* **Requirement:** This requires Teammate 2 to correctly implement the **`Content-Type`** HTTP header for all supported file types (e.g., `text/html`, `image/jpeg`). If this header is incorrect or missing, the browser will likely display the file as garbled text or fail to load it.

---

## 🛠 Team Task Breakdown

The core logic resides in two functions within `server.py` that require completion.

### 🧑‍💻 Teammate 1: HTTP Request Parsing

| Task | Location |
| :--- | :--- |
| **`parse_http_request(request_data)`** | Inside `server.py` |

**Goals:**
* Accurately decode `request_data` (bytes) to a string.
* Extract the **Requested URI** (file path) from the first line of the HTTP request.
* Handle the root request: if the URI is `/`, it must be translated to the default file (`index.html`).

### 🧑‍💻 Teammate 2: File I/O and HTTP Response Generation

| Task | Location |
| :--- | :--- |
| **`generate_http_response(file_path)`** | Inside `server.py` |

**Goals:**
* **File Read:** Safely open and read the file specified by `file_path`.
* **Content-Type (Crucial for Visual Test):** Determine the correct `Content-Type` header (e.g., `text/html`, `image/jpeg`) based on the file extension. **Hint:** Use the imported `mimetypes` library.
* **200 OK Response:** On success, build the complete response with the status line (`HTTP/1.1 200 OK`), required headers (`Content-Type`, `Content-Length`), and the file content (body) as a single `bytes` object.
* **404 Not Found:** If the file is not found, construct a **`404 Not Found`** response with an HTML body explaining the error.


### 1. What is the difference between this HTTP Server and Apache?

| Feature | This HTTP Server | Apache HTTP Server |
| :--- | :--- | :--- |
| **Abstraction** | **Low-Level** (manual socket handling, raw parsing). | **High-Level** (config-driven, abstracts networking). |
| **Concurrency** | **Single-Threaded** (one request at a time). | **Highly Concurrent** (threads/processes handle many simultaneous requests). |
| **Features** | Minimal (static file serving). | Comprehensive (caching, logging, modules, security, virtual hosts). |
| **Purpose** | Learning/Demonstration. | Production-Grade, high-scale web hosting. |

### 2. How can you write `http_server` to allow only certain browsers (e.g., Chrome) to download content?

1.  **Parse Header:** The server must **read and parse the request headers** to extract the value of the **`User-Agent`** header.
2.  **Enforce Policy (Teammate 2):** In the `generate_http_response` function:
    * **Check:** Use an `if` statement to search the extracted `User-Agent` string for allowed keywords (e.g., `"Chrome"`).
    * **Deny:** If the browser is not allowed, the server must bypass file reading and immediately send an **`HTTP/1.1 403 Forbidden`** status code in the response.
