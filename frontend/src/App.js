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
      {<PhotoPreview imgSrc={imgSrc} />}
    </div>
  );
}

export default App;
