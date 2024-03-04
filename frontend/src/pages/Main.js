import Header from '../components/Header';
import { Link } from 'react-router-dom';

const Main = () => {
    return (
        <div className='Main'>
            <Header />
            <h2>Main Page</h2>
            <Link to="/mapbox-render-line" className="btn btn-info text-white me-2">Mapbox Render Line</Link>
        </div>
    );
};

export default Main;