import { Person } from '../types/Person';

interface Props {
    show: boolean;
    onHide: () => void;
    person: Person | null;
}

export default function DetailsModal({ show, onHide, person }: Props) {
    if (!show || !person) return null;

    return (
        <div className="bg-white border-start shadow-sm d-flex flex-column px-4 py-3 mt-5 rounded-4"
             style={{ width: 340, height: 'calc(100vh - 120px)' }}
        >
            <div className="d-flex justify-content-between align-items-center mb-3">
                <h5 className="mb-0">{person.name}</h5>
                <button className="btn btn-outline-secondary" onClick={onHide}>✕</button>
            </div>

            {person.photo ? (
                <img src={person.photo} className="img-fluid rounded mb-3" alt={person.name} />
            ) : (
                <div className="bg-secondary text-white text-center py-4 rounded mb-3">No Photo</div>
            )}

            <p className="mb-0">{person.case_group}</p>
        </div>
    );
}
