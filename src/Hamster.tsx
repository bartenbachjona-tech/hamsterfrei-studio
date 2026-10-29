import React from "react";

const O = "#3A2618";
const FUR = "#E9A24E";
const BELLY = "#FFF1DC";
const PINK = "#F4A6A0";

type Props = {
  size: number;
  talking: boolean; // mouth open
  blink: boolean;
  pointerAngle: number; // degrees, extra rotation of the pointing arm
};

// Gezeichneter Hamsterfrei-Hamster (gleiche Geometrie wie im Charakterblatt, viewBox 240)
export const Hamster: React.FC<Props> = ({ size, talking, blink, pointerAngle }) => {
  const eye = (x: number, y: number) =>
    blink ? (
      <path d={`M${x - 9} ${y + 1}L${x + 9} ${y + 1}`} stroke={O} strokeWidth={4} strokeLinecap="round" />
    ) : (
      <g>
        <circle cx={x} cy={y} r={7} fill={O} />
        <circle cx={x + 2.5} cy={y - 2.5} r={2.4} fill="#FFFFFF" />
      </g>
    );

  return (
    <svg viewBox="0 0 240 240" width={size} height={size} style={{ overflow: "visible" }}>
      <ellipse cx={120} cy={224} rx={72} ry={8} fill={O} opacity={0.08} />
      <circle cx={60} cy={78} r={22} fill={FUR} stroke={O} strokeWidth={4} />
      <circle cx={180} cy={78} r={22} fill={FUR} stroke={O} strokeWidth={4} />
      <circle cx={61} cy={80} r={11} fill={PINK} />
      <circle cx={179} cy={80} r={11} fill={PINK} />
      <ellipse cx={92} cy={212} rx={17} ry={9} fill="#F4B9A0" stroke={O} strokeWidth={4} />
      <ellipse cx={148} cy={212} rx={17} ry={9} fill="#F4B9A0" stroke={O} strokeWidth={4} />
      <ellipse cx={120} cy={140} rx={80} ry={76} fill={FUR} stroke={O} strokeWidth={4} />
      <ellipse cx={120} cy={174} rx={50} ry={38} fill={BELLY} />
      <ellipse cx={120} cy={142} rx={30} ry={18} fill={BELLY} />
      <circle cx={78} cy={140} r={10} fill={PINK} opacity={0.55} />
      <circle cx={162} cy={140} r={10} fill={PINK} opacity={0.55} />
      {/* Krawatte, gelockert */}
      <g transform="rotate(-8 121 166)">
        <polygon points="114,172 128,172 137,204 121,215 106,203" fill="#24426B" stroke={O} strokeWidth={3} strokeLinejoin="round" />
        <path d="M112 186 L132 182 M109 198 L135 193" stroke="#34B27B" strokeWidth={3} fill="none" />
        <polygon points="110,159 132,159 128,172 114,172" fill="#24426B" stroke={O} strokeWidth={3} strokeLinejoin="round" />
      </g>
      <ellipse cx={82} cy={178} rx={13} ry={17} fill={FUR} stroke={O} strokeWidth={4} />
      {/* Zeigestab-Arm */}
      <g transform={`rotate(${pointerAngle} 160 162)`}>
        <line x1={166} y1={152} x2={230} y2={72} stroke="#7A4E2A" strokeWidth={5} strokeLinecap="round" />
        <circle cx={230} cy={72} r={5.5} fill="#E05A47" stroke={O} strokeWidth={2} />
        <ellipse cx={164} cy={160} rx={12} ry={17} transform="rotate(38 164 160)" fill={FUR} stroke={O} strokeWidth={4} />
      </g>
      {eye(98, 118)}
      {eye(142, 118)}
      <ellipse cx={120} cy={133} rx={6} ry={4} fill="#E58A8A" stroke={O} strokeWidth={2.5} />
      {talking ? (
        <path d="M106 141 Q120 162 134 141 Z" fill="#8A3B3B" stroke={O} strokeWidth={3.5} strokeLinejoin="round" />
      ) : (
        <g>
          <rect x={114} y={145} width={12} height={10} rx={2} fill="#FFFFFF" stroke={O} strokeWidth={2.5} />
          <path d="M120 145 L120 155" stroke={O} strokeWidth={2} />
          <path d="M108 142 Q114 150 120 143 Q126 150 132 142" fill="none" stroke={O} strokeWidth={3.5} strokeLinecap="round" />
        </g>
      )}
    </svg>
  );
};
