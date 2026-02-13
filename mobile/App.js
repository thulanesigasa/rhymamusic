import { StatusBar } from 'expo-status-bar';
import React, { useState } from 'react';
import { StyleSheet, View, SafeAreaView, Platform } from 'react-native';
import { COLORS } from './src/constants/theme';
import Header from './src/components/Header';
import Menu from './src/components/Menu';
import HomeScreen from './src/screens/HomeScreen';
import MusicScreen from './src/screens/MusicScreen';
import MerchScreen from './src/screens/MerchScreen';
import AboutScreen from './src/screens/AboutScreen';
import BookingsScreen from './src/screens/BookingsScreen';
import ContactScreen from './src/screens/ContactScreen';

export default function App() {
  const [isDarkMode, setIsDarkMode] = useState(false); // Default to Light Mode
  const [isMenuVisible, setIsMenuVisible] = useState(false);
  const [currentScreen, setCurrentScreen] = useState('Home');

  const toggleTheme = () => {
    setIsDarkMode((prev) => !prev);
  };

  const toggleMenu = () => {
    setIsMenuVisible((prev) => !prev);
  };

  const navigateTo = (screen) => {
    setCurrentScreen(screen);
    setIsMenuVisible(false);
  };

  const theme = isDarkMode ? COLORS.dark : COLORS.light;

  const renderScreen = () => {
    switch (currentScreen) {
      case 'Home':
        return <HomeScreen theme={theme} isDarkMode={isDarkMode} navigateTo={navigateTo} />;
      case 'Music':
        return <MusicScreen theme={theme} />;
      case 'Merch':
        return <MerchScreen theme={theme} />;
      case 'About':
        return <AboutScreen theme={theme} />;
      case 'Bookings':
        return <BookingsScreen theme={theme} />;
      case 'Contact':
        return <ContactScreen theme={theme} />;
      default:
        return <HomeScreen theme={theme} isDarkMode={isDarkMode} navigateTo={navigateTo} />;
    }
  };

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: theme.background }]}>
      <StatusBar style={isDarkMode ? 'light' : 'dark'} />

      {/* Header */}
      <Header
        theme={theme}
        toggleTheme={toggleTheme}
        isDarkMode={isDarkMode}
        toggleMenu={toggleMenu}
        isMenuVisible={isMenuVisible}
      />

      {/* Main Content */}
      <View style={{ flex: 1 }}>
        {renderScreen()}
      </View>

      {/* Menu Modal */}
      <Menu
        visible={isMenuVisible}
        onClose={toggleMenu}
        theme={theme}
        navigateTo={navigateTo}
      />

    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: Platform.OS === 'android' ? 25 : 0, // Basic safe area for Android
  },
});
