'use client';

import { motion, useMotionTemplate, useMotionValue } from 'framer-motion';
import { Search, MapPin, Hand } from 'lucide-react';
import { MouseEvent } from 'react';

const steps = [
    {
        id: '01',
        title: 'Search',
        description: 'Type what you need. From "AA Batteries" to "Basmati Rice".',
        icon: Search,
    },
    {
        id: '02',
        title: 'Discover',
        description: 'Instantly see which nearby shops have it in stock.',
        icon: MapPin,
    },
    {
        id: '03',
        title: 'Visit',
        description: 'Walk over, buy it, and say hello to your local shopkeeper.',
        icon: Hand,
    },
];

function Card({ step, index }: { step: typeof steps[0], index: number }) {
    const mouseX = useMotionValue(0);
    const mouseY = useMotionValue(0);

    function handleMouseMove({ currentTarget, clientX, clientY }: MouseEvent) {
        const { left, top } = currentTarget.getBoundingClientRect();
        mouseX.set(clientX - left);
        mouseY.set(clientY - top);
    }

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: index * 0.2, duration: 0.5 }}
            className="group relative border border-slate-100 bg-white rounded-[2rem] px-8 py-10 shadow-[0_8px_30px_rgb(0,0,0,0.04)] overflow-hidden"
            onMouseMove={handleMouseMove}
        >
            <motion.div
                className="pointer-events-none absolute -inset-px rounded-[2rem] opacity-0 transition duration-300 group-hover:opacity-100"
                style={{
                    background: useMotionTemplate`
                        radial-gradient(
                            650px circle at ${mouseX}px ${mouseY}px,
                            rgba(255, 107, 53, 0.15),
                            transparent 80%
                        )
                    `,
                }}
            />

            {/* Watermark Number */}
            <div className="absolute top-4 right-8 text-8xl font-black text-[#FFF5EB] group-hover:text-[#FFF0E0] transition-colors select-none">
                {step.id}
            </div>

            {/* Icon */}
            <div className="w-16 h-16 bg-[#FFF5EB] rounded-2xl flex items-center justify-center mb-8 relative z-10 group-hover:scale-110 transition-transform duration-300">
                <step.icon className="w-8 h-8 text-slate-800" strokeWidth={1.5} />
            </div>

            {/* Content */}
            <div className="relative z-10">
                <h3 className="text-2xl font-bold text-slate-900 mb-4">
                    {step.title}
                </h3>
                <p className="text-slate-500 leading-relaxed text-lg">
                    {step.description}
                </p>
            </div>
        </motion.div>
    );
}

export default function HowItWorks() {
    return (
        <section className="py-24 bg-white">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="text-center mb-20">
                    <motion.h2
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        className="text-4xl md:text-5xl font-bold text-slate-900 mb-4 tracking-tight"
                    >
                        How It Works
                    </motion.h2>
                    <motion.p
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: 0.1 }}
                        className="text-slate-500 text-lg"
                    >
                        Simple steps to support your local economy.
                    </motion.p>
                </div>

                <div className="grid md:grid-cols-3 gap-8">
                    {steps.map((step, index) => (
                        <Card key={step.id} step={step} index={index} />
                    ))}
                </div>
            </div>
        </section>
    );
}
