# Plant-Disease-Detection-Using-Azure-Cognitive-Services

**Problem Statement:**

Agriculture is the main source of food, raw material, and fuel which contributes to the economic development of a nation. Plants are highly prone to diseases that affect the growth of the plant which in turn affects the farmer. To detect a plant disease at the very initial stage, the use of plant disease detection techniques is beneficial. The symptoms of plant diseases are important in different parts of a plant such as leaves, etc. Manual detection of plant disease using leaf images is a tiresome job. Hence, it is required to develop computational methods that will make the process of disease detection and classification using leaf images. One of the methods using Azure Custom Vision API’s under Azure Cognitive Services has been proposed here. 


**Description:**

The main intention of our project is to detect the affected plant in an early stage.If the plant is affected, our proposed method will detect the type of disease like bacterial or black spots etc. Once the disease gets detected, we provide the best remedies to overcome bad conditions.

**Proposed Steps as follows:**

**1.Dataset**
For machine learning Projects, datasets play a key role. All the images collected for the dataset were downloaded from the internet especially from Kaggle official website.


**2.Azure Custom Vision API**
	Azure Custom Vision is an image recognition service that lets you build, deploy, and improve your own image identifier models. An image identifier applies labels to images, according to their detected visual characteristics. The developer, submit groups of images that feature and lack the characteristics in question. Developers label the images  at the time of submission. Then, the algorithm trains the uploaded  data and calculates its own accuracy by testing itself on those same images. Once you've trained the algorithm, you can test, retrain, and eventually use it on test images.

**3.Remedies**
	If a system detects a leaf as Apple black Spot then it will say Botyrophaeria Obtusa disease and use Liquid Sulphur copper as the remedy.

