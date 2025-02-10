"use client";

export default function GridBackground() {
  return (
    <div
      className="absolute inset-0 z-0"
      style={{
        backgroundImage: `
          linear-gradient(to right, rgba(0, 0, 0, 0.2) 1px, transparent 1px),
          linear-gradient(to bottom, rgba(0, 0, 0, 0.2) 1px, transparent 1px)
        `,
        backgroundSize: "40px 40px",
        backgroundColor: "white",
      }}
    />
  );
}