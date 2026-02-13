import React, { useRef, useEffect } from 'react';
import { View, Image, TouchableOpacity, StyleSheet, Platform, Animated, Easing } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '../constants/theme';

const HamburgerIcon = ({ isOpen, theme }) => {
    const topRotation = useRef(new Animated.Value(0)).current;
    const bottomRotation = useRef(new Animated.Value(0)).current;
    const middleOpacity = useRef(new Animated.Value(1)).current;
    const topTranslation = useRef(new Animated.Value(0)).current;
    const bottomTranslation = useRef(new Animated.Value(0)).current;

    useEffect(() => {
        const config = {
            duration: 300,
            easing: Easing.bezier(0.4, 0.0, 0.2, 1),
            useNativeDriver: true,
        };

        if (isOpen) {
            // Animate to X
            Animated.parallel([
                Animated.timing(topRotation, { ...config, toValue: 1 }),
                Animated.timing(bottomRotation, { ...config, toValue: 1 }),
                Animated.timing(middleOpacity, { ...config, toValue: 0 }),
                Animated.timing(topTranslation, { ...config, toValue: 6 }), // Move down
                Animated.timing(bottomTranslation, { ...config, toValue: -6 }), // Move up
            ]).start();
        } else {
            // Animate back to Hamburger
            Animated.parallel([
                Animated.timing(topRotation, { ...config, toValue: 0 }),
                Animated.timing(bottomRotation, { ...config, toValue: 0 }),
                Animated.timing(middleOpacity, { ...config, toValue: 1 }),
                Animated.timing(topTranslation, { ...config, toValue: 0 }),
                Animated.timing(bottomTranslation, { ...config, toValue: 0 }),
            ]).start();
        }
    }, [isOpen]);

    const topRotate = topRotation.interpolate({
        inputRange: [0, 1],
        outputRange: ['0deg', '45deg'],
    });

    const bottomRotate = bottomRotation.interpolate({
        inputRange: [0, 1],
        outputRange: ['0deg', '-45deg'],
    });

    const lineStyle = {
        height: 3,
        width: 25,
        backgroundColor: theme.text,
        borderRadius: 2,
        marginVertical: 2, // Space between lines
    };

    return (
        <View style={{ height: 24, justifyContent: 'center', alignItems: 'center' }}>
            <Animated.View
                style={[
                    lineStyle,
                    {
                        transform: [{ translateY: topTranslation }, { rotate: topRotate }],
                    },
                ]}
            />
            <Animated.View style={[lineStyle, { opacity: middleOpacity }]} />
            <Animated.View
                style={[
                    lineStyle,
                    {
                        transform: [{ translateY: bottomTranslation }, { rotate: bottomRotate }],
                    },
                ]}
            />
        </View>
    );
};

const Header = ({ theme, toggleTheme, isDarkMode, toggleMenu, isMenuVisible }) => {
    // Select the correct logo based on theme
    const logoSource = isDarkMode
        ? require('../../assets/images/curved(white).png')
        : require('../../assets/images/curved(black).png');

    return (
        <View style={[styles.container, { backgroundColor: theme.background }]}>
            {/* Logo */}
            <View style={styles.logoContainer}>
                <Image source={logoSource} style={styles.logo} resizeMode="contain" />
            </View>

            {/* Right Actions: Theme Toggle + Menu */}
            <View style={styles.actionsContainer}>
                {/* Theme Toggle Button */}
                <TouchableOpacity onPress={toggleTheme} style={styles.iconButton}>
                    <Ionicons
                        name={isDarkMode ? "moon" : "sunny"}
                        size={24}
                        color={theme.text}
                    />
                </TouchableOpacity>

                {/* Animated Hamburger Menu */}
                <TouchableOpacity style={styles.iconButton} onPress={toggleMenu} activeOpacity={0.7}>
                    <HamburgerIcon isOpen={isMenuVisible} theme={theme} />
                </TouchableOpacity>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        height: 60,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingHorizontal: 20,
        paddingTop: Platform.OS === 'android' ? 10 : 0, // Adjustment for status bar
        zIndex: 100,
    },
    logoContainer: {
        flex: 1,
    },
    logo: {
        height: 50,
        width: 120,
    },
    actionsContainer: {
        flexDirection: 'row',
        alignItems: 'center',
    },
    iconButton: {
        marginLeft: 15,
        width: 40,
        height: 40,
        justifyContent: 'center',
        alignItems: 'center',
    }
});

export default Header;
