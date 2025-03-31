export interface Person {
    _id: string;
    ovd_id: string;
    name: string;
    age: number;
    gender: string;
    citizenship: string;
    description: string;
    uk_articles: string;
    legend: string;
    case_group: string;
    case_summary: string;
    prosecution_status: string;
    detention_type: string;
    current_place_of_confinement: string;
    all_detention_measures: string;
    verdict_summary: string;
    prison_coordinates: {
        lat: number;
        lang: number;
    };
    photo: string | null;
}
