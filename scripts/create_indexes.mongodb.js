use("celebrity_matcher");

db.getCollection("celeb_images").createSearchIndex(
  "vector_index",
  "vectorSearch",
  {
    fields: [
      {
        type: "vector",
        path: "embeddings",
        numDimensions: 1024,
        similarity: "euclidean",
      },
    ],
  }
);
