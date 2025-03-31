interface Props {
    onClick: () => void;
    lat: number;
    lng: number;
}

export default function Marker({ onClick }: Props) {
    return (
        <div
            className="bg-primary rounded-circle"
            style={{ width: 16, height: 16, cursor: 'pointer' }}
            onClick={onClick}
        />
    );
}
