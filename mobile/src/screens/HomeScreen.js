import React, { useState, useCallback } from 'react';
import { View, Text, Image, TouchableOpacity, StyleSheet, Dimensions, ScrollView, Linking } from 'react-native';
import { WebView } from 'react-native-webview';
import YoutubePlayer from "react-native-youtube-iframe";
import { COLORS } from '../constants/theme';
import { Ionicons } from '@expo/vector-icons';

const { width, height } = Dimensions.get('window');

const HomeScreen = ({ theme, isDarkMode, navigateTo }) => {
    const [playing, setPlaying] = useState(false);

    const onStateChange = useCallback((state) => {
        if (state === "ended") {
            setPlaying(false);
        }
    }, []);

    const heroLogoSource = isDarkMode
        ? require('../../assets/images/rhyma(white).png')
        : require('../../assets/images/rhyma(black).png');

    const openLink = (url) => {
        Linking.openURL(url);
    };

    return (
        <ScrollView
            style={[styles.container, { backgroundColor: theme.background }]}
            nestedScrollEnabled={true}
        >
            {/* Hero Section */}
            <View style={styles.heroContainer}>
                <Image source={heroLogoSource} style={styles.heroLogo} resizeMode="contain" />

                <Text style={[styles.tagline, { color: theme.text }]}>
                    Defining the New Sound of Luxury
                </Text>

                <TouchableOpacity style={styles.ctaButton} onPress={() => navigateTo && navigateTo('Music')}>
                    <Text style={styles.ctaText}>Listen Now</Text>
                </TouchableOpacity>

                {/* Social Icons Row */}
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
                </View>
            </View>

            {/* New Release Video */}
            <View style={styles.sectionContainer}>
                <Text style={[styles.sectionTitle, { color: theme.text }]}>New Release Video</Text>
                <View style={{ height: 220, width: '100%', borderRadius: 12, overflow: 'hidden', backgroundColor: '#000' }}>
                    <YoutubePlayer
                        height={220}
                        play={playing}
                        videoId={"prZ-ErkCkNw"}
                        onChangeState={onStateChange}
                        webViewProps={{
                            androidLayerType: 'hardware' // Improves performance on Android
                        }}
                    />
                </View>
                <TouchableOpacity onPress={() => openLink('https://youtube.com/rhymangn')} style={{ marginTop: 15, flexDirection: 'row', alignItems: 'center' }}>
                    <Text style={{ color: theme.text, fontSize: 16, marginRight: 8 }}>Stream on YouTube</Text>
                    <Ionicons name="logo-youtube" size={20} color={COLORS.light.accent} />
                </TouchableOpacity>
            </View>

            {/* Featured Projects */}
            <View style={styles.sectionContainer}>
                <Text style={[styles.sectionTitle, { color: theme.text }]}>Featured Projects</Text>

                {/* Stand Out Album */}
                <View style={styles.albumContainer}>
                    <TouchableOpacity onPress={() => openLink('https://open.spotify.com/album/11G7xf6VQHjhSSCtW6FRdt')} style={styles.titleContainer}>
                        <Text style={[styles.embedTitle, { color: theme.text }]}>STAND OUT</Text>
                        <Ionicons name="open-outline" size={18} color={theme.text} style={{ marginLeft: 5 }} />
                    </TouchableOpacity>

                    <View style={{ height: 380, borderRadius: 12, overflow: 'hidden', backgroundColor: 'transparent' }}>
                        <WebView
                            source={{
                                html: `
                      <html>
                        <head>
                          <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
                          <style>
                            /* Move scrollbar to left */
                            html, body { height: 100%; direction: rtl; margin: 0; padding: 0; }
                            /* Restore content direction */
                            .content { height: 100%; direction: ltr; }
                          </style>
                        </head>
                        <body style="background-color:transparent;">
                           <div class="content">
                               <iframe style="border-radius:12px" src="https://open.spotify.com/embed/album/11G7xf6VQHjhSSCtW6FRdt?utm_source=generator" width="100%" height="100%" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
                           </div>
                        </body>
                      </html>
                    ` }}
                            style={{ flex: 1, backgroundColor: 'transparent' }}
                            scrollEnabled={true}
                            nestedScrollEnabled={true}
                            originWhitelist={['*']}
                        />
                    </View>
                    <TouchableOpacity style={styles.smallCta} onPress={() => openLink('https://music.apple.com/za/album/stand-out/1815679533')}>
                        <Ionicons name="logo-apple" size={20} color="#fff" style={{ marginRight: 8 }} />
                        <Text style={styles.smallCtaText}>Stand Out on Apple Music</Text>
                    </TouchableOpacity>
                </View>

                {/* Stamina Album */}
                <View style={[styles.albumContainer, { marginTop: 40 }]}>
                    <TouchableOpacity onPress={() => openLink('https://open.spotify.com/album/3YUXPunrRpyRj2zv3ufbEQ')} style={styles.titleContainer}>
                        <Text style={[styles.embedTitle, { color: theme.text }]}>STAMINA</Text>
                        <Ionicons name="open-outline" size={18} color={theme.text} style={{ marginLeft: 5 }} />
                    </TouchableOpacity>

                    <View style={{ height: 380, borderRadius: 12, overflow: 'hidden', backgroundColor: 'transparent' }}>
                        <WebView
                            source={{
                                html: `
                      <html>
                        <head>
                          <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
                          <style>
                            /* Move scrollbar to left */
                            html, body { height: 100%; direction: rtl; margin: 0; padding: 0; }
                            /* Restore content direction */
                            .content { height: 100%; direction: ltr; }
                          </style>
                        </head>
                        <body style="background-color:transparent;">
                           <div class="content">
                               <iframe style="border-radius:12px" src="https://open.spotify.com/embed/album/3YUXPunrRpyRj2zv3ufbEQ?utm_source=generator" width="100%" height="100%" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
                           </div>
                        </body>
                      </html>
                    ` }}
                            style={{ flex: 1, backgroundColor: 'transparent' }}
                            scrollEnabled={true}
                            nestedScrollEnabled={true}
                            originWhitelist={['*']}
                        />
                    </View>
                    <TouchableOpacity style={styles.smallCta} onPress={() => openLink('https://music.apple.com/za/album/stamina/1676464008')}>
                        <Ionicons name="logo-apple" size={20} color="#fff" style={{ marginRight: 8 }} />
                        <Text style={styles.smallCtaText}>Stamina on Apple Music</Text>
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
    heroContainer: {
        height: height * 0.7,
        justifyContent: 'center',
        alignItems: 'center',
        paddingHorizontal: 20,
    },
    heroLogo: {
        width: width * 0.8,
        height: 120,
        marginBottom: 20,
    },
    tagline: {
        fontSize: 18,
        textAlign: 'center',
        marginBottom: 30,
        fontWeight: '300',
        letterSpacing: 1,
    },
    ctaButton: {
        backgroundColor: COLORS.light.accent,
        paddingVertical: 12,
        paddingHorizontal: 30,
        borderRadius: 25,
        marginBottom: 30,
    },
    ctaText: {
        color: '#FFFFFF',
        fontSize: 16,
        fontWeight: '600',
        textTransform: 'uppercase',
    },
    socialRow: {
        flexDirection: 'row',
        marginTop: 20,
    },
    socialIcon: {
        marginHorizontal: 10,
    },
    sectionContainer: {
        paddingVertical: 30,
        paddingHorizontal: 15, // Reduced horizontal padding slightly to enlarge content
        alignItems: 'center',
        width: '100%',
    },
    sectionTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 20,
        textTransform: 'uppercase',
        letterSpacing: 1,
    },
    albumContainer: {
        width: '100%',
        // minHeight for the embed
    },
    smallCta: {
        marginTop: 10,
        backgroundColor: COLORS.light.accent,
        padding: 12,
        borderRadius: 8,
        alignItems: 'center',
        flexDirection: 'row', // Align icon and text
        justifyContent: 'center',
    },
    smallCtaText: {
        color: '#fff',
        fontWeight: 'bold',
    },
    titleContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 10,
        alignSelf: 'flex-start',
        paddingLeft: 5,
    },
    embedTitle: {
        fontSize: 18,
        fontWeight: '700',
        textTransform: 'uppercase',
        letterSpacing: 1,
    }
});

export default HomeScreen;
