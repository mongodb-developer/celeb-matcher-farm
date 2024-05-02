import "./PhotoPreview.css";

import React from "react";
import CircumIcon from "@klarr-agency/circum-icons-react";

function PhotoPreview({ imgSrc }) {
  const showing = imgSrc !== null;
  return (
    <div className="PhotoPreview">
      <div className={showing ? "frame showing" : "frame"}>
        <img src={imgSrc} className="image" alt="You, possibly." />
        <button className="upload">Find Your Celebrity Lookalike!</button>
      </div>
    </div>
  );
}

export default PhotoPreview;
