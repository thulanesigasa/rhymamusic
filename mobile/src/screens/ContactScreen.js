import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TextInput, TouchableOpacity, Linking } from 'react-native';
import { COLORS } from '../constants/theme';
import { Ionicons } from '@expo/vector-icons';
import CustomAlert from '../components/CustomAlert';

const ContactScreen = ({ theme }) => {
    const [alertVisible, setAlertVisible] = useState(false);
    const [alertConfig, setAlertConfig] = useState({ title: '', message: '' });

    const [formData, setFormData] = useState({
        name: '',
        email: '',
        message: ''
    });

    const showAlert = (title, message) => {
        setAlertConfig({ title, message });
        setAlertVisible(true);
    };

    const handleSubmit = () => {
        const { name, email, message } = formData;
        if (!name || !email || !message) {
            showAlert('Missing Fields', 'Please fill in all fields.');
            return;
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            showAlert('Invalid Email', 'Please enter a valid email address.');
            return;
        }

        const subject = `Inquiry from ${name}`;
        const body = `Name: ${name}\nEmail: ${email}\n\nMessage:\n${message}`;

        Linking.openURL(`mailto:enquiries@rhymamusic.co.za?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`)
            .then(() => {
                showAlert('Thank You', 'We have received your message.');
                setFormData({
                    name: '',
                    email: '',
                    message: ''
                });
            })
            .catch(() => {
                showAlert('Error', 'Could not open email app.');
            });
    };

    const openLink = (url) => {
        Linking.openURL(url);
    };

    return (
        <ScrollView style={[styles.container, { backgroundColor: theme.background }]} contentContainerStyle={styles.contentContainer}>
            <CustomAlert
                visible={alertVisible}
                title={alertConfig.title}
                message={alertConfig.message}
                onClose={() => setAlertVisible(false)}
                theme={theme}
            />
            <Text style={[styles.heading, { color: theme.text }]}>Get in Touch</Text>
            <Text style={[styles.subText, { color: theme.text }]}>For general inquiries, press, and collaborations.</Text>

            <View style={styles.form}>
                <Text style={[styles.label, { color: theme.text }]}>Name</Text>
                <TextInput
                    style={[styles.input, { color: theme.text, borderColor: theme.text, backgroundColor: theme.secondaryBg }]}
                    value={formData.name}
                    onChangeText={(text) => setFormData({ ...formData, name: text })}
                />

                <Text style={[styles.label, { color: theme.text }]}>Email</Text>
                <TextInput
                    style={[styles.input, { color: theme.text, borderColor: theme.text, backgroundColor: theme.secondaryBg }]}
                    keyboardType="email-address"
                    value={formData.email}
                    onChangeText={(text) => setFormData({ ...formData, email: text })}
                />

                <Text style={[styles.label, { color: theme.text }]}>Message</Text>
                <TextInput
                    style={[styles.input, { color: theme.text, borderColor: theme.text, backgroundColor: theme.secondaryBg, height: 120 }]}
                    multiline
                    value={formData.message}
                    onChangeText={(text) => setFormData({ ...formData, message: text })}
                />

                <TouchableOpacity style={styles.button} onPress={handleSubmit}>
                    <Text style={styles.buttonText}>Send Message</Text>
                </TouchableOpacity>
            </View>

            <View style={styles.connectSection}>
                <Text style={[styles.connectTitle, { color: theme.text }]}>Connect</Text>
                <View style={styles.socialRow}>
                    <TouchableOpacity onPress={() => openLink('https://x.com/rhymangn')}>
                        <Ionicons name="logo-twitter" size={24} color={theme.text} style={styles.socialIcon} />
                    </TouchableOpacity>
                    <TouchableOpacity onPress={() => openLink('https://music.apple.com/us/artist/rhyma/1232075857')}>
                        <Ionicons name="logo-apple" size={24} color={theme.text} style={styles.socialIcon} />
                    </TouchableOpacity>
                    <TouchableOpacity onPress={() => openLink('https://www.tiktok.com/@rhymangn')}>
                        <Ionicons name="logo-tiktok" size={24} color={theme.text} style={styles.socialIcon} />
                    </TouchableOpacity>
                    <TouchableOpacity onPress={() => openLink('https://www.instagram.com/rhymangn')}>
                        <Ionicons name="logo-instagram" size={24} color={theme.text} style={styles.socialIcon} />
                    </TouchableOpacity>
                    <TouchableOpacity onPress={() => openLink('https://youtube.com/rhymangn')}>
                        <Ionicons name="logo-youtube" size={24} color={theme.text} style={styles.socialIcon} />
                    </TouchableOpacity>
                    <TouchableOpacity onPress={() => openLink('https://open.spotify.com/search/RHYMA')}>
                        <Ionicons name="musical-notes" size={24} color={theme.text} style={styles.socialIcon} />
                    </TouchableOpacity>
                </View>
            </View>

            <View style={{ height: 50 }} />
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    contentContainer: {
        padding: 20,
        alignItems: 'center',
    },
    heading: {
        fontSize: 28,
        fontWeight: 'bold',
        marginBottom: 10,
        marginTop: 20,
        textAlign: 'center',
    },
    subText: {
        marginBottom: 30,
        opacity: 0.7,
    },
    form: {
        width: '100%',
    },
    label: {
        marginBottom: 8,
        fontWeight: '600',
    },
    input: {
        borderWidth: 1,
        padding: 12,
        marginBottom: 20,
        borderRadius: 6,
    },
    button: {
        backgroundColor: COLORS.light.accent,
        padding: 15,
        alignItems: 'center',
        borderRadius: 6,
        marginTop: 10,
    },
    buttonText: {
        color: '#fff',
        fontWeight: 'bold',
        fontSize: 16,
        textTransform: 'uppercase',
    },
    connectSection: {
        marginTop: 50,
        alignItems: 'center',
    },
    connectTitle: {
        fontSize: 20,
        fontWeight: 'bold',
        marginBottom: 20,
    },
    socialRow: {
        flexDirection: 'row',
    },
    socialIcon: {
        marginHorizontal: 12,
    }
});

export default ContactScreen;
