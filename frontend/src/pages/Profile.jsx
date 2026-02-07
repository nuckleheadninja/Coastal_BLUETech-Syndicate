import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

const Profile = ({ apiUrl = 'http://localhost:8000' }) => {
    const { user, logout } = useAuth();
    const [reports, setReports] = useState([]);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('reports');

    useEffect(() => {
        const fetchMyReports = async () => {
            try {
                const response = await axios.get(`${apiUrl}/api/reports/my`);
                setReports(response.data);
                setLoading(false);
            } catch (error) {
                console.error("Error fetching reports:", error);
                setLoading(false);
            }
        };

        fetchMyReports();
    }, [apiUrl]);

    if (!user) return null;

    return (
        <div style={styles.page}>
            <div style={styles.container}>
                {/* Profile Header */}
                <div className="premium-card" style={styles.profileHeader}>
                    <div style={styles.avatar}>
                        {user.full_name?.charAt(0) || 'U'}
                    </div>
                    <div style={styles.userInfo}>
                        <h1 style={styles.userName}>{user.full_name}</h1>
                        <p style={styles.userEmail}>{user.email}</p>
                        <div style={styles.badge}>
                            {user.role === 'admin' ? '🛡️ System Admin' : '🌊 Coastal Guardian'}
                        </div>
                    </div>
                </div>

                {/* Tabs */}
                <div style={styles.tabContainer}>
                    <button
                        style={{ ...styles.tab, ...(activeTab === 'reports' ? styles.activeTab : {}) }}
                        onClick={() => setActiveTab('reports')}
                    >
                        My Reports ({reports.length})
                    </button>
                    <button
                        style={{ ...styles.tab, ...(activeTab === 'settings' ? styles.activeTab : {}) }}
                        onClick={() => setActiveTab('settings')}
                    >
                        Account Settings
                    </button>
                </div>

                {/* Content */}
                {activeTab === 'reports' ? (
                    <div style={styles.reportsGrid}>
                        {loading ? (
                            <p>Loading your reports...</p>
                        ) : reports.length > 0 ? (
                            reports.map(report => (
                                <div key={report.id} className="premium-card" style={styles.reportCard}>
                                    <div style={styles.reportImageWrapper}>
                                        <img src={`${apiUrl}${report.image_path}`} alt="Pollution" style={styles.reportImage} />
                                        <div style={styles.statusBadge(report.status)}>
                                            {report.status || 'pending'}
                                        </div>
                                    </div>
                                    <div style={styles.reportContent}>
                                        <div style={styles.reportType}>{report.pollution_type.replace('_', ' ')}</div>
                                        <div style={styles.reportDate}>{new Date(report.created_at).toLocaleDateString()}</div>
                                        <p style={styles.reportDesc}>
                                            {report.description || "No description provided."}
                                        </p>
                                        {report.ngo_name && (
                                            <div style={styles.forwardInfo}>
                                                Forwarded to: <strong>{report.ngo_name}</strong>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            ))
                        ) : (
                            <div style={styles.emptyState}>
                                <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📸</div>
                                <h3>No reports yet</h3>
                                <p>Help protect our oceans by reporting pollution you see.</p>
                            </div>
                        )}
                    </div>
                ) : (
                    <div className="premium-card" style={styles.settingsCard}>
                        <h3>Profile Information</h3>
                        <div style={styles.infoRow}>
                            <label>Full Name</label>
                            <input type="text" value={user.full_name} readOnly style={styles.input} />
                        </div>
                        <div style={styles.infoRow}>
                            <label>Email Address</label>
                            <input type="email" value={user.email} readOnly style={styles.input} />
                        </div>
                        <div style={styles.infoRow}>
                            <label>Account Role</label>
                            <input type="text" value={user.role} readOnly style={styles.input} />
                        </div>
                        <button className="btn-primary" style={{ marginTop: '1rem' }} onClick={() => alert("Feature coming soon!")}>
                            Edit Profile
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

const styles = {
    page: {
        minHeight: '100vh',
        background: '#f8fafc',
        padding: '2rem 1rem',
    },
    container: {
        maxWidth: '1000px',
        margin: '0 auto',
    },
    profileHeader: {
        display: 'flex',
        alignItems: 'center',
        gap: '2rem',
        padding: '3rem',
        marginBottom: '2rem',
        background: 'linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%)',
    },
    avatar: {
        width: '100px',
        height: '100px',
        borderRadius: '50%',
        background: 'linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '3rem',
        fontWeight: 'bold',
        color: 'white',
        boxShadow: '0 10px 25px -5px rgba(14, 165, 233, 0.4)',
    },
    userInfo: {
        flex: 1,
    },
    userName: {
        fontSize: '2.5rem',
        fontWeight: '800',
        color: '#0f172a',
        marginBottom: '0.25rem',
    },
    userEmail: {
        fontSize: '1.1rem',
        color: '#64748b',
        marginBottom: '1rem',
    },
    badge: {
        display: 'inline-block',
        padding: '0.35rem 1rem',
        background: 'rgba(14, 165, 233, 0.1)',
        color: '#0ea5e9',
        borderRadius: '2rem',
        fontSize: '0.9rem',
        fontWeight: '700',
    },
    tabContainer: {
        display: 'flex',
        gap: '1rem',
        marginBottom: '2rem',
        borderBottom: '1px solid #e2e8f0',
        paddingBottom: '0.5rem',
    },
    tab: {
        background: 'none',
        border: 'none',
        padding: '0.75rem 1.5rem',
        fontSize: '1rem',
        fontWeight: '600',
        color: '#64748b',
        cursor: 'pointer',
        transition: 'all 0.2s',
        borderRadius: '0.5rem',
    },
    activeTab: {
        color: '#0ea5e9',
        background: 'rgba(14, 165, 233, 0.05)',
    },
    reportsGrid: {
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
        gap: '2rem',
    },
    reportCard: {
        padding: 0,
        overflow: 'hidden',
    },
    reportImageWrapper: {
        position: 'relative',
        height: '200px',
    },
    reportImage: {
        width: '100%',
        height: '100%',
        objectFit: 'cover',
    },
    statusBadge: (status) => ({
        position: 'absolute',
        top: '1rem',
        right: '1rem',
        padding: '0.25rem 0.75rem',
        borderRadius: '1rem',
        fontSize: '0.75rem',
        fontWeight: '800',
        textTransform: 'uppercase',
        background: status === 'resolved' ? '#dcfce7' : status === 'forwarded' ? '#dbeafe' : '#fef9c3',
        color: status === 'resolved' ? '#166534' : status === 'forwarded' ? '#1e40af' : '#854d0e',
        boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)',
    }),
    reportContent: {
        padding: '1.5rem',
    },
    reportType: {
        fontSize: '1.25rem',
        fontWeight: '800',
        color: '#0f172a',
        textTransform: 'capitalize',
        marginBottom: '0.25rem',
    },
    reportDate: {
        fontSize: '0.85rem',
        color: '#94a3b8',
        marginBottom: '1rem',
    },
    reportDesc: {
        fontSize: '0.95rem',
        color: '#475569',
        lineHeight: 1.5,
        marginBottom: '1rem',
    },
    forwardInfo: {
        fontSize: '0.85rem',
        padding: '0.75rem',
        background: '#f8fafc',
        borderRadius: '0.5rem',
        border: '1px solid #e2e8f0',
    },
    emptyState: {
        gridColumn: '1 / -1',
        textAlign: 'center',
        padding: '5rem 0',
        color: '#94a3b8',
    },
    settingsCard: {
        maxWidth: '600px',
    },
    infoRow: {
        marginBottom: '1.5rem',
    },
    input: {
        width: '100%',
        padding: '0.75rem',
        background: '#f1f5f9',
        border: '1px solid #e2e8f0',
        borderRadius: '0.5rem',
        marginTop: '0.5rem',
        color: '#475569',
        fontWeight: '600',
    }
};

export default Profile;
