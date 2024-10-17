import "./PhotoPreview.css";

import React from "react";
import Button from "@leafygreen-ui/button";

function PhotoPreview({ imgSrc, onClick }) {
  const showing = imgSrc !== null;
  return (
    <div className="PhotoPreview">
      <div className={showing ? "frame showing" : "frame"}>
        <img src={imgSrc} className="image" alt="You, possibly." />
        <p style={{textAlign: "center"}}>
        <Button variant="primary" onClick={onClick}>
          Find Your Celebrity Lookalike!
        </Button>
        </p>
      </div>
    </div>
  );
}

export default PhotoPreview;
