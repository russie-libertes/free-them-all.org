import { Person } from '../types/Person';

interface Props {
    show: boolean;
    onHide: () => void;
    people: Person[];
    onPersonClick: (person: Person) => void;
}

export default function FilterModal({ show, onHide, people, onPersonClick }: Props) {
    if (!show) return null;

    return (
        <div
            className="bg-white shadow-sm d-flex flex-column px-4 py-3 mt-5 rounded-4"
            style={{ width: 340, height: 'calc(100vh - 120px)' }}
        >
            <div className="d-flex justify-content-between align-items-center mb-3">
                <input className="form-control me-2" placeholder="Поиск по имени..." />
                <button className="btn btn-outline-secondary" onClick={onHide}>✕</button>
            </div>

            <div className="flex-grow-1 overflow-auto">
                {people.map(person => (
                    <div
                        key={person._id}
                        className="border rounded p-2 mb-3"
                        style={{ cursor: 'pointer' }}
                        onClick={() => onPersonClick(person)}
                    >
                        <div className="fw-bold">{person.name}</div>
                        <div className="text-muted small">{person.description}</div>
                    </div>
                ))}
            </div>
        </div>
    );
}
