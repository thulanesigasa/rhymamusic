import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TextInput, TouchableOpacity, Linking } from 'react-native';
import { COLORS } from '../constants/theme';
import CustomAlert from '../components/CustomAlert';

const BookingsScreen = ({ theme }) => {
    const [alertVisible, setAlertVisible] = useState(false);
    const [alertConfig, setAlertConfig] = useState({ title: '', message: '' });

    const [formData, setFormData] = useState({
        contactPerson: '',
        eventDate: '',
        venueName: '',
        budget: '',
        details: ''
    });

    const showAlert = (title, message) => {
        setAlertConfig({ title, message });
        setAlertVisible(true);
    };

    const handleSubmit = () => {
        const { contactPerson, eventDate, venueName, budget, details } = formData;
        if (!contactPerson || !eventDate || !venueName) {
            showAlert('Missing Fields', 'Please fill in the required fields.');
            return;
        }

        const subject = `Booking Inquiry: ${eventDate} @ ${venueName}`;
        const body = `Contact Person: ${contactPerson}\nEvent Date: ${eventDate}\nVenue: ${venueName}\nBudget: R${budget}\n\nDetails:\n${details}`;

        Linking.openURL(`mailto:bookings@rhymamusic.co.za?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`)
            .then(() => {
                showAlert('Thank You', 'We have received your booking inquiry.');
                setFormData({
                    contactPerson: '',
                    eventDate: '',
                    venueName: '',
                    budget: '',
                    details: ''
                });
            })
            .catch(() => {
                showAlert('Error', 'Could not open email app.');
            });
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
            <Text style={[styles.heading, { color: theme.text }]}>Bookings & Inquiries</Text>
            <Text style={[styles.subText, { color: theme.text }]}>For bookings, appearances, and features.</Text>

            <View style={styles.form}>
                <Text style={[styles.label, { color: theme.text }]}>Contact Person / Promoter</Text>
                <TextInput
                    style={[styles.input, { color: theme.text, borderColor: theme.text, backgroundColor: theme.secondaryBg }]}
                    value={formData.contactPerson}
                    onChangeText={(text) => setFormData({ ...formData, contactPerson: text })}
                />

                <Text style={[styles.label, { color: theme.text }]}>Event Date</Text>
                <TextInput
                    style={[styles.input, { color: theme.text, borderColor: theme.text, backgroundColor: theme.secondaryBg }]}
                    placeholder="YYYY-MM-DD"
                    placeholderTextColor="#999"
                    value={formData.eventDate}
                    onChangeText={(text) => setFormData({ ...formData, eventDate: text })}
                />

                <Text style={[styles.label, { color: theme.text }]}>Venue Name & Location</Text>
                <TextInput
                    style={[styles.input, { color: theme.text, borderColor: theme.text, backgroundColor: theme.secondaryBg }]}
                    value={formData.venueName}
                    onChangeText={(text) => setFormData({ ...formData, venueName: text })}
                />

                <Text style={[styles.label, { color: theme.text }]}>Budget Offer (ZAR)</Text>
                <TextInput
                    style={[styles.input, { color: theme.text, borderColor: theme.text, backgroundColor: theme.secondaryBg }]}
                    placeholder="e.g. 50000"
                    placeholderTextColor="#999"
                    keyboardType="numeric"
                    value={formData.budget}
                    onChangeText={(text) => setFormData({ ...formData, budget: text })}
                />

                <Text style={[styles.label, { color: theme.text }]}>Additional Details</Text>
                <TextInput
                    style={[styles.input, { color: theme.text, borderColor: theme.text, backgroundColor: theme.secondaryBg, height: 100 }]}
                    multiline
                    value={formData.details}
                    onChangeText={(text) => setFormData({ ...formData, details: text })}
                />

                <TouchableOpacity style={styles.button} onPress={handleSubmit}>
                    <Text style={styles.buttonText}>Submit Inquiry</Text>
                </TouchableOpacity>
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
    }
});

export default BookingsScreen;
