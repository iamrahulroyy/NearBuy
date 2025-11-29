'use client';

import { useEffect, useState } from 'react';
import { motion, useMotionValue, useSpring } from 'framer-motion';

export default function CustomCursor() {
    const [isHovered, setIsHovered] = useState(false);
    const [isVisible, setIsVisible] = useState(false);
    const [isMobile, setIsMobile] = useState(false);
    const [isInActiveSection, setIsInActiveSection] = useState(false);

    const cursorX = useMotionValue(-100);
    const cursorY = useMotionValue(-100);

    const springConfig = { damping: 25, stiffness: 700 };
    const cursorXSpring = useSpring(cursorX, springConfig);
    const cursorYSpring = useSpring(cursorY, springConfig);

    useEffect(() => {
        // Check if device is mobile/touch device
        const checkMobile = () => {
            const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
            const isMobileWidth = window.innerWidth < 768; // md breakpoint
            setIsMobile(isTouchDevice || isMobileWidth);
        };

        checkMobile();
        window.addEventListener('resize', checkMobile);

        // If mobile, don't show cursor
        if (isMobile) {
            return () => {
                window.removeEventListener('resize', checkMobile);
            };
        }

        const moveCursor = (e: MouseEvent) => {
            cursorX.set(e.clientX);
            cursorY.set(e.clientY);
            if (!isVisible) setIsVisible(true);

            // Check if cursor is over specific sections with data attribute
            const target = e.target as HTMLElement;
            const activeSectionElement =
                target.closest('[data-cursor-section="hero"]') ||
                target.closest('[data-cursor-section="content"]');

            const isInSpecificSection = activeSectionElement !== null;

            setIsInActiveSection(isInSpecificSection);
        };

        const handleMouseEnter = () => setIsHovered(true);
        const handleMouseLeave = () => setIsHovered(false);

        window.addEventListener('mousemove', moveCursor);

        // Add event listeners to clickable elements
        const clickables = document.querySelectorAll('a, button, input, textarea, select, [role="button"]');
        clickables.forEach((el) => {
            el.addEventListener('mouseenter', handleMouseEnter);
            el.addEventListener('mouseleave', handleMouseLeave);
        });

        // MutationObserver to handle dynamic content
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    const newClickables = document.querySelectorAll('a, button, input, textarea, select, [role="button"]');
                    newClickables.forEach((el) => {
                        el.removeEventListener('mouseenter', handleMouseEnter);
                        el.removeEventListener('mouseleave', handleMouseLeave);
                        el.addEventListener('mouseenter', handleMouseEnter);
                        el.addEventListener('mouseleave', handleMouseLeave);
                    });
                }
            });
        });

        observer.observe(document.body, { childList: true, subtree: true });

        return () => {
            window.removeEventListener('mousemove', moveCursor);
            window.removeEventListener('resize', checkMobile);
            clickables.forEach((el) => {
                el.removeEventListener('mouseenter', handleMouseEnter);
                el.removeEventListener('mouseleave', handleMouseLeave);
            });
            observer.disconnect();
        };
    }, [cursorX, cursorY, isVisible, isMobile]);

    // Don't render on mobile or if not visible or not in active section
    if (isMobile || !isVisible || !isInActiveSection) return null;

    return (
        <div className="pointer-events-none fixed inset-0 z-[9999] overflow-hidden">
            {/* Main Dot */}
            <motion.div
                className="absolute h-3 w-3 rounded-full bg-[#FF6B35]"
                style={{
                    x: cursorX,
                    y: cursorY,
                    translateX: '-50%',
                    translateY: '-50%',
                }}
            />

            {/* Trailing Glow */}
            <motion.div
                className="absolute rounded-full border border-[#FF6B35] bg-[#FF6B35]/10 backdrop-blur-[1px]"
                style={{
                    x: cursorXSpring,
                    y: cursorYSpring,
                    translateX: '-50%',
                    translateY: '-50%',
                    height: isHovered ? 64 : 32,
                    width: isHovered ? 64 : 32,
                }}
                transition={{
                    type: 'spring',
                    damping: 20,
                    stiffness: 300,
                }}
            />
        </div>
    );
}
