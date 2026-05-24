import ProfileForm from '../../components/ProfileForm';
import CVUploadPanel from '../../components/CVUploadPanel';

export default function ProfilePage() {
    return (
        <div>
            <h1>Profile</h1>
            <ProfileForm />
            <CVUploadPanel />
        </div>
    );
}
