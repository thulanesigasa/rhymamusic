import React from 'react';
import { Modal, View, Text, TouchableOpacity, StyleSheet, Dimensions } from 'react-native';
import { COLORS } from '../constants/theme';
import { Ionicons } from '@expo/vector-icons';

const { width, height } = Dimensions.get('window');

const CustomAlert = ({ visible, title, message, onClose, theme }) => {
    if (!visible) return null;

    return (
        <Modal
            transparent={true}
            visible={visible}
            animationType="fade"
            onRequestClose={onClose}
        >
            <View style={styles.overlay}>
                <View style={[styles.alertBox, { backgroundColor: theme.background, borderColor: theme.text }]}>
                    <View style={styles.iconContainer}>
                        <Ionicons name="mail-unread-outline" size={48} color={COLORS.light.accent} />
                    </View>
                    <Text style={[styles.title, { color: theme.text }]}>{title}</Text>
                    <Text style={[styles.message, { color: theme.text }]}>{message}</Text>

                    <TouchableOpacity style={styles.button} onPress={onClose}>
                        <Text style={styles.buttonText}>OK</Text>
                    </TouchableOpacity>
                </View>
            </View>
        </Modal>
    );
};

const styles = StyleSheet.create({
    overlay: {
        flex: 1,
        backgroundColor: 'rgba(0,0,0,0.7)',
        justifyContent: 'center',
        alignItems: 'center',
    },
    alertBox: {
        width: width * 0.85,
        padding: 24,
        borderRadius: 16,
        borderWidth: 1,
        alignItems: 'center',
        shadowColor: "#000",
        shadowOffset: {
            width: 0,
            height: 4,
        },
        shadowOpacity: 0.30,
        shadowRadius: 4.65,
        elevation: 8,
    },
    iconContainer: {
        marginBottom: 16,
    },
    title: {
        fontSize: 22,
        fontWeight: 'bold',
        marginBottom: 12,
        textAlign: 'center',
        textTransform: 'uppercase',
        letterSpacing: 1,
    },
    message: {
        fontSize: 16,
        textAlign: 'center',
        marginBottom: 24,
        opacity: 0.8,
        lineHeight: 22,
    },
    button: {
        backgroundColor: COLORS.light.accent,
        paddingVertical: 12,
        paddingHorizontal: 32,
        borderRadius: 8,
        width: '100%',
        alignItems: 'center',
    },
    buttonText: {
        color: '#fff',
        fontWeight: 'bold',
        fontSize: 16,
        textTransform: 'uppercase',
    }
});

export default CustomAlert;
