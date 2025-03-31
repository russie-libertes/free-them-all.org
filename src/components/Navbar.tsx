interface Props {
    onSearchClick: () => void;
}

export default function Navbar({ onSearchClick }: Props) {
    return (
        <div className="navbar navbar-expand-lg navbar-light bg-white shadow-sm px-5 py-3 rounded-4">
            <a className="navbar-brand fw-bold" href="#">MyMapApp</a>
            <div className="ms-auto d-flex align-items-center gap-3">
                <button className="btn btn-outline-primary">Главная</button>
                <button className="btn btn-primary" onClick={onSearchClick}>Поиск</button>
            </div>
        </div>
    );
}
