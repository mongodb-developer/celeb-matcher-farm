//import logo from './logo.svg';
import "./App.css";

import React from "react";
import Webcam from "react-webcam";
import CircumIcon from "@klarr-agency/circum-icons-react";
import PhotoPreview from "./PhotoPreview";

function isLandscape() {
  return window.screen.orientation.type.startsWith("landscape");
}

function App() {
  const [imgSrc, setImgSrc] = React.useState(null);
  const [orientation, setOrientation] = React.useState(
    isLandscape() ? "landscape" : "portrait"
  );
  const [loading, setLoading] = React.useState(false);
  const [lookalikes, setLookalikes] = React.useState(null);
  const [description, setDescription] = React.useState(null);
  const onOrientationChange = () => {
    console.log("Orientation Change", isLandscape());
    setOrientation(isLandscape() ? "landscape" : "portrait");
  };

  React.useEffect(
    () => (
      onOrientationChange(),
      window.screen.orientation.addEventListener("change", onOrientationChange),
      () =>
        window.screen.orientation.removeEventListener(
          "change",
          onOrientationChange
        )
    ),
    []
  );

  let aspectRatio;
  if (orientation === "landscape") {
    aspectRatio = 4 / 3;
  } else {
    aspectRatio = 3 / 4;
  }
  const videoConstraints = {
    facingMode: "user",
    aspectRatio,
  };

  const uploadHandler = async () => {
    setLoading(true);
    const result = await fetch("/api/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        img: imgSrc,
      }),
    });
    const data = await result.json();
    setLoading(false);

    setDescription(data.description);
    setLookalikes(data.images);

    console.log("Done");
  };

  return (
    <div className="App">
      <h1>Celebrity Lookalike!</h1>
      <p>First take a photo...</p>
      <Webcam
        audio={false}
        screenshotFormat="image/jpeg"
        forceScreenshotSourceSize={true}
        videoConstraints={videoConstraints}
        width="100%"
        className="Webcam"
      >
        {({ getScreenshot }) => (
          <button
            className="PhotoButton"
            onClick={() => {
              console.log(navigator.mediaDevices.getSupportedConstraints());
              setImgSrc(getScreenshot());
            }}
          >
            <CircumIcon name="camera" />
          </button>
        )}
      </Webcam>

      {<PhotoPreview imgSrc={imgSrc} onClick={uploadHandler} />}
      {loading && <div>Loading ...</div>}

      {lookalikes &&
        lookalikes.map((imageData, index) => {
          return (
            <div key={index} className="lookalike">
              <h2>You look like...</h2>
              <img src={"data:image/jpeg;base64, " + imageData} />
            </div>
          );
        })}

      {description && (
        <div class="description">
          <h2>Description:</h2>
          <p>{description}</p>
        </div>
      )}
    </div>
  );
}

export default App;
