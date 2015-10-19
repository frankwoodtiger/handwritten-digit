# handwritten-digit
An handwritten recognition web app with the use of cgi-scripts

<p>Start of the web app</p>
<img src='/img/handwritten-init.png?raw=true' alt="1" height="400px" width='400'>

<p>Recognition of digit</p>
<img src='/img/handwritten-1.png?raw=true' alt="1" height="400px" width='400'>

<img src='/img/handwritten-2.png?raw=true' alt="2" height="400px" width='400'>

<img src='/img/handwritten-3.png?raw=true' alt="6" height="400px" width='400'>

<ol><b>This webapp consists of two major parts as shown below</b>
  <li>UI logic
    <ol>
      <li>index.html - the actual UI in HTML</li>
      <li>paint.js - Control of HTML Canvas that lets users to write the handwritten digit to be tested</li>
      <li>button-logic.js - handling the AJAX request to those Python CGI neural network scripts</li>
      <li>iteration-slider.js - responsible for the slider that shows training iteration</li>
    </ol>
  </li>
  <li>Python CGI script to handle the neural network for recognizing handwritten digit
    <ol>
      <li>*-ubyte - actual training set of size 50,000  and test sample set of size 10,000 with total 60,000 28x28 images used by the neural network</li>
      <li>thetas.mat - the actual trained weight matrix used for prediction</li>
      <li>feedforward-prediction-cgi.py - loads the matrix in thetas.mat, and perform feedfoward prediction using the matrix.</li>
      <li>train-handwritten-digit-cgi.py - trains the weight matrix and save it to thetas.mat</li>
      <li>imshow-grayscale-mat.py - saves the raw pixel data under the CGI dir for debugging purpose.</li>
    </ol>
  </li>
</ol>

<ul><b>Proof of concept</b>
  <li>Use of AJAX and JQuery to achieve rich interaction interface.</li>
  <li>Use of HTML Canvas and event-driven programming</li>
  <li>Use of Python CGI script</li>
  <li>Demonstration of practical use of neural network for basic image recognition</li>
</ul>

<ul><b>Notes</b>
  <li>One must configure their Apache server to enable the use of CGI script</li>
  <li>In order to have a working training functionality, timeout must be disable for the long loading time that might occur during the NN training stage</li>
</ul>
