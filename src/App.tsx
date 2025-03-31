import { useState } from 'react';
import GoogleMapReact from 'google-map-react';
import Navbar from './components/Navbar';
import FilterModal from './components/FilterModal';
import DetailsModal from './components/DetailsModal';
import Marker from './components/Marker';
import dummyPeople from './data/dummyPeople';
import { Person } from './types/Person';

export default function App() {
    const [showFilterModal, setShowFilterModal] = useState(true);
    const [showDetailsModal, setShowDetailsModal] = useState(false);
    const [selectedPerson, setSelectedPerson] = useState<Person | null>(null);

    const handlePersonClick = (person: Person) => {
        setSelectedPerson(person);
        setShowDetailsModal(true);
        setShowFilterModal(true);
    };

    return (
        <div className="container-fluid p-0" style={{ height: '100vh', overflow: 'hidden', position: 'relative' }}>
            <div className="position-absolute z-3" style={{ top: '20px', left: '20px', right: '20px' }}>
                <Navbar onSearchClick={() => setShowFilterModal(true)} />
            </div>

            {showFilterModal && (
                <div className="position-absolute  z-2 mt-5" style={{ top: '10px', left: '20px' }}>
                    <FilterModal
                        show={showFilterModal}
                        onHide={() => {
                            setShowFilterModal(false);
                            setShowDetailsModal(false);
                        }}
                        people={dummyPeople}
                        onPersonClick={handlePersonClick}
                    />
                </div>
            )}

            {showDetailsModal && (
                <div className="position-absolute z-2 mt-5 " style={{ top: '10px', left: '370px' }}>
                    <DetailsModal
                        show={showDetailsModal}
                        onHide={() => setShowDetailsModal(false)}
                        person={selectedPerson}
                    />
                </div>
            )}

            <div className="w-100 h-100">
                <GoogleMapReact
                    bootstrapURLKeys={{ key: process.env.REACT_APP_GOOGLE_MAPS_API_KEY || '' }}
                    defaultCenter={{ lat: 41.7151, lng: 44.8271 }}
                    defaultZoom={12}
                >
                    {dummyPeople.map((person) => (
                        <Marker
                            key={person._id}
                            lat={person.prison_coordinates.lat}
                            lng={person.prison_coordinates.lang}
                            onClick={() => handlePersonClick(person)}
                        />
                    ))}
                </GoogleMapReact>
            </div>
        </div>
    );
}
