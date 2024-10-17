import { H2, Body } from "@leafygreen-ui/typography";
import Card from "@leafygreen-ui/card";

export default function SimilarAttendees(props) {
  return (
    <Card>
      <H2>Other attendee lookalikes</H2>
      <Body>Can you find them at the event?</Body>
      <div className="similarattendees_row">
      {props?.similarAttendees?.map((imageData, index) => {
        return (
          <div className="similarattendees_col">
            <img src={"data:image/jpeg;base64, " + imageData.image} alt="Lookalike" />
          </div>
        )
      })
      }
      </div>
    </Card>
  );
}