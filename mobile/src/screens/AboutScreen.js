import React from 'react';
import { View, Text, StyleSheet, ScrollView, Image } from 'react-native';
import { COLORS } from '../constants/theme';

const AboutScreen = ({ theme }) => {
    return (
        <ScrollView style={[styles.container, { backgroundColor: theme.background }]} contentContainerStyle={styles.contentContainer}>
            <Text style={[styles.heading, { color: theme.text }]}>Biography</Text>

            <Image
                source={require('../../assets/images/Untitled.jpeg')}
                style={styles.profileImage}
                resizeMode="cover"
            />

            <View style={styles.textContainer}>
                <Text style={[styles.subHeading, { color: COLORS.light.accent }]}>RHYMA (Charlie Inyang)</Text>

                <Text style={[styles.paragraph, { color: theme.text }]}>
                    <Text style={{ fontWeight: 'bold' }}>RHYMA</Text>, a Nigerian-born recording artist based in Gauteng, South Africa, is redefining
                    African urban music. Known for his dynamic blend of <Text style={{ fontWeight: 'bold' }}>Afrobeats, Pop, Commercial House, and New
                        Age</Text> sounds, he represents a new generation of artists pushing boundaries while honoring
                    their African heritage.
                </Text>

                <Text style={[styles.paragraph, { color: theme.text }]}>
                    From his beginnings with the a cappella group <Text style={{ fontStyle: 'italic' }}>Soul Healers</Text> to launching his solo career in
                    2014, RHYMA has crafted a versatile sound inspired by legends like <Text style={{ fontWeight: 'bold' }}>Fela Kuti, Brenda Fassie, and
                        Bob Marley</Text>. His music resonates with themes of love, ambition, and freedom.
                </Text>

                <Text style={[styles.paragraph, { color: theme.text }]}>
                    His discography includes the debut album <Text style={{ fontStyle: 'italic' }}>'Fly With You'</Text> (2019) and EPs <Text style={{ fontStyle: 'italic' }}>'Ambition'</Text>
                    (2020) and <Text style={{ fontStyle: 'italic' }}>'Vibes on Vibes'</Text> (2025). He kicked off 2026 with the single
                    <Text style={{ fontWeight: 'bold' }}> 'Medusa'</Text>, featuring Sjijo and Jack Jakalas, exploring the eccentric 3-Step sound.
                </Text>

                <Text style={[styles.quote, { color: theme.text }]}>
                    "Music is not just sound, it's an architecture of emotion."
                </Text>
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
        fontSize: 32,
        fontWeight: '300',
        marginBottom: 30,
        textTransform: 'uppercase',
        letterSpacing: 2,
        textAlign: 'center',
    },
    profileImage: {
        width: '100%',
        height: 300,
        borderRadius: 12,
        marginBottom: 30,
    },
    textContainer: {
        width: '100%',
    },
    subHeading: {
        fontSize: 22,
        fontWeight: 'bold',
        marginBottom: 20,
    },
    paragraph: {
        fontSize: 16,
        lineHeight: 24,
        marginBottom: 20,
        opacity: 0.9,
    },
    quote: {
        fontSize: 18,
        fontStyle: 'italic',
        fontWeight: 'bold',
        marginTop: 20,
        textAlign: 'center',
    }
});

export default AboutScreen;
