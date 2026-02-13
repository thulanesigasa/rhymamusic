import React from 'react';
import { View, Text, TouchableOpacity, Modal, StyleSheet, Dimensions, Platform, Linking } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '../constants/theme';

const { width, height } = Dimensions.get('window');

const Menu = ({ visible, onClose, theme, navigateTo }) => {
    const openLink = (url) => {
        Linking.openURL(url);
    };

    return (
        <Modal
            visible={visible}
            animationType="fade"
            transparent={false}
            presentationStyle="fullScreen"
            onRequestClose={onClose}
        >
            <View style={[styles.container, { backgroundColor: theme.background }]}>
                {/* Close Button */}
                <View style={styles.headerSpacer}>
                    <TouchableOpacity onPress={onClose} style={styles.closeButton}>
                        <Ionicons name="close" size={32} color={theme.text} />
                    </TouchableOpacity>
                </View>

                {/* Menu Items */}
                <View style={styles.menuItems}>
                    <TouchableOpacity style={styles.menuItem} onPress={() => navigateTo('Home')}>
                        <Text style={[styles.menuText, { color: theme.text }]}>Home</Text>
                    </TouchableOpacity>

                    <TouchableOpacity style={styles.menuItem} onPress={() => navigateTo('Music')}>
                        <Text style={[styles.menuText, { color: theme.text }]}>Music</Text>
                    </TouchableOpacity>

                    <TouchableOpacity style={styles.menuItem} onPress={() => navigateTo('Merch')}>
                        <Text style={[styles.menuText, { color: theme.text }]}>Merch</Text>
                    </TouchableOpacity>

                    <TouchableOpacity style={styles.menuItem} onPress={() => navigateTo('About')}>
                        <Text style={[styles.menuText, { color: theme.text }]}>About</Text>
                    </TouchableOpacity>

                    <TouchableOpacity style={styles.menuItem} onPress={() => navigateTo('Bookings')}>
                        <Text style={[styles.menuText, { color: theme.text }]}>Bookings</Text>
                    </TouchableOpacity>

                    <TouchableOpacity style={styles.menuItem} onPress={() => navigateTo('Contact')}>
                        <Text style={[styles.menuText, { color: theme.text }]}>Contact</Text>
                    </TouchableOpacity>
                </View>

                {/* Footer Info & Socials */}
                <View style={styles.footer}>
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
                            {/* Using musical-notes as a generic fallback or custom if avail, standard Ionicons doesn't have spotify logo in all libraries */}
                            <Ionicons name="musical-notes" size={24} color={theme.text} style={styles.socialIcon} />
                        </TouchableOpacity>
                    </View>

                    <Text style={[styles.footerText, { color: theme.text, opacity: 0.6 }]}>
                        RHYMA &copy; {new Date().getFullYear()}
                    </Text>
                </View>
            </View>
        </Modal>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        paddingTop: Platform.OS === 'android' ? 40 : 50,
        paddingHorizontal: 20,
    },
    headerSpacer: {
        height: 60,
        justifyContent: 'center',
        alignItems: 'flex-end',
    },
    closeButton: {
        padding: 5,
        marginTop: 10, // Adjust to match header vertical alignment
    },
    menuItems: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    menuItem: {
        paddingVertical: 15,
        width: '100%',
        alignItems: 'center',
    },
    menuText: {
        fontSize: 28,
        fontWeight: '300',
        letterSpacing: 2,
        textTransform: 'uppercase',
    },
    footer: {
        marginBottom: 60,
        alignItems: 'center',
    },
    footerText: {
        fontSize: 12,
    },
    socialRow: {
        flexDirection: 'row',
        marginBottom: 20,
    },
    socialIcon: {
        marginHorizontal: 12,
    }
});

export default Menu;
