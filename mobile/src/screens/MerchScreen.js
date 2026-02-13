import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TextInput, TouchableOpacity, Linking } from 'react-native';
import { COLORS } from '../constants/theme';
import CustomAlert from '../components/CustomAlert';

const MerchScreen = ({ theme }) => {
    const [alertVisible, setAlertVisible] = useState(false);
    const [alertConfig, setAlertConfig] = useState({ title: '', message: '' });

    const showAlert = (title, message) => {
        setAlertConfig({ title, message });
        setAlertVisible(true);
    };

    const handleNotify = async () => {
        const email = 'newrelease@rhymamusic.co.za';
        const subject = 'Notify Me: Rhyma Merch Drop';
        const body = 'Hi Rhyma Team,\n\nPlease notify me when the new merchandise drop goes live.\n\nThanks!';
        const url = `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;

        const canOpen = await Linking.canOpenURL(url);

        if (canOpen) {
            Linking.openURL(url);
            // Show alert slightly after to simulating "sending" action initiating
            setTimeout(() => {
                showAlert('Thank You', 'We have received your notification request.');
            }, 500);
        } else {
            showAlert('Error', 'Could not open email app.');
        }
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
            <Text style={[styles.heading, { color: theme.text }]}>Merchandise</Text>

            {/* Coming Soon Container */}
            <View style={styles.comingSoonContainer}>
                <Text style={[styles.comingSoonTitle, { color: COLORS.light.accent }]}>Coming Soon</Text>
                <Text style={[styles.description, { color: theme.text }]}>
                    Exclusive <Text style={{ fontWeight: 'bold' }}>Rhyma</Text> apparel and accessories are currently in production.
                    Prices will be listed in ZAR (Rands).
                </Text>

                {/* Notify Form */}
                <View style={[styles.notifyBox, { backgroundColor: theme.secondaryBg }]}>
                    <Text style={[styles.notifyText, { color: theme.text }]}>GET NOTIFIED WHEN THE DROP GOES LIVE</Text>

                    <TouchableOpacity style={styles.button} onPress={handleNotify}>
                        <Text style={styles.buttonText}>Notify Me via Email</Text>
                    </TouchableOpacity>
                </View>
            </View>
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
        justifyContent: 'center',
        minHeight: '80%',
    },
    heading: {
        fontSize: 32,
        fontWeight: '300',
        marginBottom: 40,
        textTransform: 'uppercase',
        letterSpacing: 2,
        textAlign: 'center',
    },
    comingSoonContainer: {
        alignItems: 'center',
        width: '100%',
    },
    comingSoonTitle: {
        fontSize: 48,
        fontWeight: 'bold',
        marginBottom: 20,
        textAlign: 'center',
    },
    description: {
        fontSize: 16,
        textAlign: 'center',
        marginBottom: 40,
        lineHeight: 24,
        opacity: 0.8,
    },
    notifyBox: {
        padding: 20,
        width: '100%',
        borderWidth: 1,
        borderColor: '#ccc',
        borderRadius: 8,
    },
    notifyText: {
        fontSize: 14,
        fontWeight: 'bold',
        marginBottom: 15,
        textAlign: 'center',
        letterSpacing: 1,
    },
    input: {
        borderWidth: 1,
        padding: 15,
        marginBottom: 15,
        borderRadius: 4,
    },
    button: {
        backgroundColor: COLORS.light.accent,
        padding: 15,
        alignItems: 'center',
        borderRadius: 4,
    },
    buttonText: {
        color: '#fff',
        fontWeight: 'bold',
        textTransform: 'uppercase',
    }
});

export default MerchScreen;
