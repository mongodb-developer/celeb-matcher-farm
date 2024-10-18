import { H2, H3 } from "@leafygreen-ui/typography";
import Card from "@leafygreen-ui/card";

export default function Lookalikes(props) {
  return (
    <Card>
      <H2>You look like...</H2>
      {props?.lookalikes?.map((imageData, index) => {
        return (
          <div className="celeblookalike">
            <img src={"data:image/jpeg;base64, " + imageData.image} alt="Lookalike" />
            <H3>{imageData.name}</H3>
          </div>
        )
      })
      }
    </Card>
  );
}