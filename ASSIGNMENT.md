## **Take-Home Project**

This exercise is designed to help us evaluate your backend engineering skills, focusing on API design, concurrency handling, and problem-solving in a distributed environment.

The goal is to create a minimal URL shortener service that meets the outlined requirements. You are encouraged to spend a couple of hours on this, aiming for a functional MVP that you’ll demonstrate and discuss during your technical interview.

---

### **Project Description**

Implement a URL shortener service that exposes the following API endpoints:

- **`POST /url/shorten`**  
  Accepts a full URL (e.g., `https://www.reevv.com`) and returns a shortened URL (e.g., `http://localhost:8000/r/abc`).  
  - Input: JSON payload containing the `url` key
  - Output: JSON response with the `short_url` key, e.g., `{"short_url": "http://localhost:8000/r/abc"}`

- **`GET /r/<short_url>`**  
  Resolves the short URL to its original form.  
  - Output: HTTP 302 redirect to the original URL or 404 if the short URL is unknown.

### **Core Requirements**

1. **Data Persistence Across Instances**  
   The shortened URL should be retrievable from any instance of the service. For example, if a URL is shortened via one instance, it should be accessible from other instances. 

2. **Concurrency and Multiple Workers**  
   Design the service to handle multiple workers. For this, a distributed database or persistent storage is recommended.

3. **Performance and Scalability**  
   Use an efficient method for generating unique short URLs, keeping in mind scalability if the service were to grow over time.

4. **API Specifications**  
   Adhere to HTTP standards, including correct status codes and error messages.

---

### **Getting Started**

1. Clone this repository:

2. The repository includes a skeleton of the URL Shortener service, with the following:
   - `server.py`: Contains FastAPI-based route skeletons
   - `Makefile`: Facilitates Docker builds and commands
   - `Dockerfile`: Simplifies containerization if needed

3. You are encouraged to use this FastAPI setup and Dockerfile, but feel free to implement the service in a way that best suits your approach. Please ensure any changes to setup or execution steps are reflected in the README.



### **Evaluation Criteria**

Your submission will be assessed based on:

1. **Functionality and Completeness**  
   - Meeting all requirements for URL shortening and redirection
   - Efficient and scalable short URL generation
   - Robust handling of edge cases and invalid inputs

2. **Code Quality and Best Practices**  
   - Clear, well-organized code that follows Python and FastAPI best practices
   - Thoughtful design decisions, with clean, modular, and maintainable code

3. **Testing and Error Handling**  
   - Unit tests for core functionalities (e.g., URL shortening, retrieval, and invalid requests)
   - Comprehensive error handling with meaningful messages

4. **Documentation**  
   - Clear README instructions on setup, running, and testing
   - Explanations of design choices and trade-offs in your README or comments


### **Additional if you have time**

- **Custom Short URLs**: Allow users to specify a custom short URL slug (e.g., `/r/my-custom-url`).
- **Expiration**: Add an expiration mechanism for short URLs (e.g., URLs expire after a specified duration).
- **Analytics**: Include a tracking mechanism to record how many times each short URL is accessed.
- **Rate Limiting**: Prevent abuse by limiting the rate of URL shortening requests per user or IP address.

---

### **Submission Guidelines**

1. **README Documentation**: Ensure your README is complete, detailing:
   - Setup and execution steps
   - Explanations of design decisions and trade-offs
   - Any deviations from the original requirements or additional features added
   - Create your own repository and push up the code please send a link to josh@reevv.com. DO NOT MAKE A PULL REQUEST

2. **Testing Instructions**: Provide instructions or Postman collections for testing the endpoints.

### **Next Steps**

Be prepared to demo your solution, explain your decisions, and work through further scenarios or live coding challenges based on this project.

Good luck! We look forward to seeing your approach and discussing your solution!

