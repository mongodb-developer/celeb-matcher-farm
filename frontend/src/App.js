import "./App.css";
import { H1, H2, Body } from "@leafygreen-ui/typography";
import Card from "@leafygreen-ui/card";
import Logo from "@leafygreen-ui/logo";
import Button from "@leafygreen-ui/button";
import Icon from "@leafygreen-ui/icon";

import Lookalikes from "./components/Lookalikes";
import PhotoPreview from "./components/PhotoPreview";

import React from "react";
import Webcam from "react-webcam";

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

  const reset = () => {
    setLookalikes(null);
    setDescription(null);
  }

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
  };

  return (
    <div className="App">
      <Logo></Logo><H1 className="app-heading">Celebrity Lookalike!</H1>
      <Card>
      <p><Body baseFontSize={16}>First take a photo...</Body></p>
      <Webcam
        audio={false}
        screenshotFormat="image/jpeg"
        forceScreenshotSourceSize={true}
        videoConstraints={videoConstraints}
        width="100%"
        className="Webcam"
      >
        {({ getScreenshot }) => (
          <p style={{"textAlign": "center"}}>
          <Button
            aria-label="Take photo"
            onClick={() => {
              reset();
              setImgSrc(getScreenshot());
            }}
            variant="primary"
          >
            <Icon glyph="Camera" size={32} />
          </Button>
          </p>
        )}
      </Webcam>
      </Card>

      {<PhotoPreview imgSrc={imgSrc} onClick={uploadHandler} />}

      <div className="results-area">
        {loading ? (
          <div className="loading">
            <img src="/loading-explain.gif" alt="Loading..." />
          </div>
        ) : (
          <>
            {lookalikes &&
              <Lookalikes lookalikes={lookalikes} />
            }
            <p></p>


            {description && (
              <Card>
                <H2>Description:</H2>
                <Body baseFontSize={16}>{description}</Body>
              </Card>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default App;
