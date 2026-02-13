import React from 'react';
import { View, Text, StyleSheet, ScrollView, Dimensions, TouchableOpacity, Linking } from 'react-native';
import { WebView } from 'react-native-webview';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '../constants/theme';

const { width } = Dimensions.get('window');

const SpotifyEmbed = ({ uri, title, link }) => {
    // Construct the embed HTML manually to ensure it looks like the web version
    const htmlContent = `
      <html>
        <head><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0"></head>
        <body style="margin:0;padding:0;background-color:transparent;">
          <iframe style="border-radius:12px" src="${uri}" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
        </body>
      </html>
    `;

    const openLink = () => {
        if (link) {
            Linking.openURL(link);
        }
    };

    return (
        <View style={styles.embedContainer}>
            {title && (
                <TouchableOpacity onPress={openLink} style={styles.titleContainer}>
                    <Text style={styles.embedTitle}>{title}</Text>
                    <Ionicons name="open-outline" size={16} color={COLORS.light.text} style={{ marginLeft: 5 }} />
                </TouchableOpacity>
            )}
            <WebView
                originWhitelist={['*']}
                source={{ html: htmlContent }}
                style={styles.webview}
                scrollEnabled={false}
                nestedScrollEnabled={true}
            />
        </View>
    );
};

const MusicScreen = ({ theme }) => {
    return (
        <ScrollView
            style={[styles.container, { backgroundColor: theme.background }]}
            nestedScrollEnabled={true}
        >
            <Text style={[styles.heading, { color: theme.text }]}>Top Tracks</Text>

            {/* Medusa */}
            <SpotifyEmbed
                title="Medusa - Radio Edit"
                link="https://open.spotify.com/track/2tYZv2w593ANPrz1HZhp55"
                uri="https://open.spotify.com/embed/track/2tYZv2w593ANPrz1HZhp55?utm_source=generator&theme=0"
            />

            {/* I'm Calling (Album/Track) */}
            <SpotifyEmbed
                title="I'm Callin'"
                link="https://open.spotify.com/album/0u14DjLpxYnzJzHdnV1Ez1"
                uri="https://open.spotify.com/embed/album/0u14DjLpxYnzJzHdnV1Ez1?utm_source=generator&theme=0"
            />

            {/* Stamina (Track) */}
            <SpotifyEmbed
                title="Stamina"
                link="https://open.spotify.com/track/3b3VmMwvuKGPDNcUdYmLBh"
                uri="https://open.spotify.com/embed/track/3b3VmMwvuKGPDNcUdYmLBh?utm_source=generator&theme=0"
            />

            <Text style={[styles.heading, { color: theme.text, marginTop: 30 }]}>Latest EP</Text>

            {/* Stand Out EP */}
            <View style={[styles.embedContainer, { height: 'auto' }]}>
                <TouchableOpacity onPress={() => Linking.openURL('https://open.spotify.com/album/4zdanK4qRRjCe0N4XXToBt')} style={styles.titleContainer}>
                    <Text style={styles.embedTitle}>STAND OUT</Text>
                    <Ionicons name="open-outline" size={16} color={theme.text} style={{ marginLeft: 5 }} />
                </TouchableOpacity>
                <View style={{ height: 380, width: '100%', borderRadius: 12, overflow: 'hidden' }}>
                    <WebView
                        originWhitelist={['*']}
                        source={{
                            html: `
                    <html>
                        <head>
                        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
                        <style>
                            html, body { height: 100%; direction: rtl; margin: 0; padding: 0; }
                            .content { height: 100%; direction: ltr; }
                        </style>
                        </head>
                        <body style="background-color:transparent;">
                        <div class="content">
                            <iframe style="border-radius:12px" src="https://open.spotify.com/embed/album/4zdanK4qRRjCe0N4XXToBt?utm_source=generator" width="100%" height="100%" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
                        </div>
                        </body>
                    </html>
                    ` }}
                        style={styles.webview}
                        scrollEnabled={true}
                        nestedScrollEnabled={true}
                    />
                </View>
            </View>

            <View style={{ height: 50 }} />
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        paddingVertical: 20,
        paddingHorizontal: 10, // Reduced from 20 to 10 to enlarge embeds
    },
    heading: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 20,
        fontFamily: 'System',
        textAlign: 'center',
        textTransform: 'uppercase',
        letterSpacing: 1,
    },
    embedContainer: {
        width: '100%',
        marginBottom: 20,
        backgroundColor: 'transparent',
        borderRadius: 12,
        overflow: 'visible', // Changed to visible for title
    },
    webview: {
        backgroundColor: 'transparent',
        flex: 1,
    },
    titleContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'flex-start',
        marginBottom: 8,
        marginLeft: 4,
    },
    embedTitle: {
        fontSize: 16,
        fontWeight: '600',
        color: COLORS.light.text, // Will need handling for dark mode if passed as prop, using variable for now
        textTransform: 'uppercase',
        letterSpacing: 0.5,
    }
});

export default MusicScreen;
