import Header from '../components/Header';
import { Link } from 'react-router-dom';

const Main = () => {
    return (
        <div className='Main'>
            <Header />
            <h2>Main Page</h2>
            <Link to="/test-map" className="btn btn-info text-white me-2">Test Rendering Map</Link>
        </div>
    );
};

export default Main;