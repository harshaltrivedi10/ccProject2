Representative Performance Evaluator

#Background

Speaker recognition and identification is a booming research field, where many companies have put forward their technologies, using state-of-the-art machine learning techniques to perform speaker identification. The state-of-the-art Microsoft’s Speaker Recognition API is used to enroll speakers using an audio. And later when an audio is provided as an input to its Speaker Identification API, the API returns the Identification Profile ID of the enrollment it matches with. There is one project that I came across in this field of study [4]. This system is a Web Application that uses Microsoft’s Speaker Recognition API and lets users submit audio to enroll and identify people, but that is what it does, there are no more functionalities in this project.

The problem that I are trying to address goes beyond the concept of just speaker recognition and speaker identification. I want to address the problem of evaluating the performance of customer service representatives while they are conversing with the customers of a particular company. I didn’t come across any system that performs both speaker recognition / identification along with evaluating the performance of the person who is speaking and by performance the project just focuses on how well the customer representatives have spoken to the customers and do they use keywords or key-phrases which create a sense of satisfaction in the customers.

Though there have been many speaker recognition and identification projects, there hasn’t been any project which, along with identifying the speaker, also gives scores based on what and how they make a conversation. In today’s world, in order for a business to sustain, it is very important that businesses retain their customers. Customer satisfaction plays a huge role in growth of a business and its strong base is built from a very good customer support team. Our application looks to take a step towards evaluating the performance customer service representatives perform. These performance reports can lead to making decisions to improve the training of customer representatives, change modules of their training, and make changes in the leadership as well.
 
#Design and Implementation

3.1) Architecture and Design
The above figure shows the architecture of the project. The major components of the project include the cloud services provided by Google Cloud Platform like Google App Engine (GAE) which is a Platform as Service (PaaS), Google Cloud Store (GCS), and Cloud Firestore. In this project, Google App Engine (GAE) was used in the standard mode to host the entire web application. I also used Cloud Firestore for our application in the Native mode, which provided a flexible, scalable, cloud-hosted, and NoSQL database. I also used Google Cloud Storage (GCS) to store the enrollment audios and the conversational audios in which the customer representative needed to be identified and a report was to be generated. I also used Google Cloud Storage (GCS) to store the reports generated for all the customer representatives. Microsoft’s Speaker Recognition service was used to implement the feature of enrolling and recognizing a customer representative based on their voice. Finally, Google’s Speech-to-Text API service was used to generate the transcript from the conversational audio which was then used to find the performance of the representative. The web application was hosted on Google App Engine (GAE) using a Flask server. The web page of the application which was the frontend part was developed using Javascript, HTML and CSS. The backend of the project was developed using Python with the help of different types of libraries like Pandas, http, and urllib.

3.2) Autoscaling

As the web application was hosted on Google App Engine (GAE), the auto scaling was performed by the App Engine scheduler which manages the number of dynamic instances based on the volume of requests being made to the web application.  The scaling type of our web application was automatic which was specified in app.yaml. It also consisted of a threshold of different types of metrics on which the app engine scheduler would use to scale-out or scale-in the number of instances. The app.yaml file in our application included matrices like “target_cpu_utilization”, “min_instances”, “max_instances”, “min_pending latency”, “max_pending_latency”, and  “max_concurrent_requests'' with certain threshold values for app engine scheduler to perform autoscaling.

3.3) Implementation of other components

3.3.1) Microsoft Azure Speaker Recognition API
Microsoft provides cloud-based Speaker Recognition APIs that contain advanced AI algorithms for speaker verification and speaker identification. In our implementation, I have focused on using the Speaker Identification API. 

3.3.1.1) Speaker Identification
Speaker identification is of the utmost importance when an audi is provided and the user wants to know who is speaking. The whole process of Speaker Identification is carried out in two phases: Speaker Enrollment and Speaker Identification. These steps are explained individually in detail below:

3.3.1.1.1) Enrollment:
In this phase, an audio is provided to the API and the features are extracted from it, these features would then be used to identify a person. The audio that is provided as an input to this API can contain any kind of text, the content, i.e., what a person talks about in the audio is not important, making this part content-independent. Complex AI and Machine Learning Algorithms run in the background and they extract necessary features from the audio, such that it can be used in future to identify who is talking. Though there’s no restriction on content in the audio, there are specific instructions on what sort of audio has to be provided as an input and what format it should have, these characteristics are:
    WAV Container
    PCM Encoding
    16K Rate 
    16 bit Sample format
    Mono channel

On successful enrollment, an identification profile id is mapped to that audio recording and returned as a response. 

3.3.1.1.2) Identification:
In this phase, an audio is provided as an input, the content of which can be way different from the content provided during the Enrollment phase. From this audio, features are extracted and they are matched with the features of every enrolled identification profile id in the account. The identification profile id which is closed to the given audio is returned. This says that the Identification API thinks the returned Identification profile id is closest to the given audio and he or she is the speaker in this audio.

3.3.2) Google’s Speech to Text API
Google Speech-to-Text API is used to generate transcripts of audio files. This API has support of more than 100 languages. I used this API to generate transcripts of the audio that I provided as an input. I used this transcript to know how many keywords or key-phrases are spoken by the person and in doing so I generate their performance report and compare their scores with the mean scores of all the identified and evaluated persons till date.

3.3.3) Google’s Cloud Firestore
I used Cloud Firestore to enable the system to handle unstructured data. I used to type of collections in Firestore. The first one mapped the identification profile id to a person’s name, so I could identify who is speaking, based on the identification profile id returned by Microsoft’s Speech Recognition API. The second collection was used to store the keywords or key-phrases along with their frequencies, i.e., how many times they occur in an audio. This was stored for each individual speaker.

3.3.4) Google’s Cloud Datastore
I used Datastore to make two buckets. The first bucket was used to store all the audio files to be used for Speaker Enrollment and Speaker Identification purposes. The audio files to be used for Enrollment were named using the following format “FirstName.wav”, where FirstName was the name of the speaker. The test audio files were named as “test#.wav” where test# where # is a placeholder for numbers 1, 2, 3 and so on. The second bucket was used to store the generated reports for all the representatives who have been evaluated and store their performance scores there.

3.4) Uniqueness of the Solution
During the initial stage of the project, I analyzed different type of Point of Sale(POS) systems in place at different markets, and stores and I found that none of such system providers provided a way or a matrix to determine the performance of the employees working on the floor and the employees having a direct conversation with the customers. Hence by having a system like this, it will become very easy to evaluate the performance of the customer representatives in a very simple and efficient way by using a web application hosted on Google Cloud Platform which a manager/owner of the store will have access to. The web application will also be fast, reliable and highly available because by the use of Google App Engine, it will scale itself in all the zones of a region and will also scale automatically based on traffic and latency to serve the customers in a better way.































Yoshitha Gajula:
    The project targets utilizing the platform as a service cloud computing innovation to send a self assembled real-world application and naturally scale it dependent on request. The resources used are Microsoft’s Azure, Google’s Speech to text and Google App Engine. It is an analysis for customer representatives on how well they are performing and finally generating a report for the same. Below are my contributions to each of the phases(Design, Implementation and Testing).
    In the design phase I first discussed the resources to be used such as Microsoft azure for speaker identification and Google’s text to speech API for speech extraction from the audio files. And later finalized the architecture of the project. It is called Representative performance Evaluator where I evaluate each representatives performance using the above resources and generate a report. I worked on finalizing the architecture and also how the Microsoft Azure works and all. Initially I evaluated all the cloud services and created a free tier account in Microsoft Azure with 200$ credits as free. Also, I was involved in evaluating database design options such as RDBMS or NOSQL. And decided to use Firestore, Cloud Firestore is an adaptable, versatile database for portable, web, and server advancement from Firebase and Google Cloud Platform.
    In the Implementation stage, I was associated with the usage of Microsoft's Speaker recognition API. I have contributed to the work on user identification and enrollment. The code for the part of the system was written in Python programming language using libraries like os, http, urllib, json, io and pandas. Examining different kinds of situations, for example, where there are multiple users speaking and etc., Additionally studied different auto scaling parameters for the Google App Engine and tried them in different situations. Peruse the documentation for Google cloud to help in setting up the App Engine. Coordinated the backend Flask Code with the frontend javascript interface. Also worked on Google’s text to speech API and integrated it with the existing code. Figured out the major drawbacks of using Microsoft’s speaker recognition API and wrote the code accordingly. I also worked on the comparison between different speech to text API’S like Amazon Web Service's Transcribe, PicoVoices’s Cheetah, IBM’s Watson Speech to Text, and decided to go with Google’s API since it is working efficiently and giving the results according to the project perspective and requirement.    
    The testing fundamentally included two stages, one was unit testing performed after development or setup of a prerequisite and the other stage was incorporation testing known as integration testing which was performed once the entire application was constructed. In the main stage I took a shot at parts where I did the implementation and furthermore tested every other person's components to discover bugs assuming any. When the components were created at each phase of incorporation I tested the components again to check whether there is no breakage. I also tested various use cases in the form of different audio inputs in speaker recognition API and Google’s speech to text API.I also worked on finding the effectiveness and the correctness of the API that I were using like what was the recognition success ratio when I were using Microsoft.s Speaker Recognition API for identifying the customer representative. I also researched and experimented with different types of audio files to check the effectiveness and the correctness of the transcript generated by Google's Speech to Text API.
     I also made the structure of the document and wrote the report for providing the update of the work that I had done till the halfway reporting. Mainly, I analyzed the features and the part of the projects that were completed and the parts which were left to be implemented. I also contributed for the final part of the project which is Project Report. I took the initiative and started writing the report and also included the architecture diagram which I drew in visio.io  according to the project. 
