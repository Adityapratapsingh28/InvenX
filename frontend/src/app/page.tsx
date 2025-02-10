"use client";
import { motion, useMotionValue, useTransform } from "framer-motion";
import { BlurText } from "@/components/BlurText";
import { Navbar } from "@/components/Navbar";
import { Send, Truck, Package, BoxesIcon, BarChart3, Factory, Globe, Cloud, Shield, Zap, Database } from "lucide-react";
import GridBackground from "@/components/GridBackground";
import { useState } from "react";
import FeatureCard from '@/components/FeatureCard';

export default function Home() {
  const features = [
    {
      title: "Optimal Warehouse-Assortment Selection",
      description: "Predicts regional demand using historical sales and external factors, with AI-driven inventory placement recommendations",
      icon: <Truck className="w-6 h-6 text-blue-600" />,
      link: "/features/logistics",
      imageUrl: "https://thumbs.dreamstime.com/b/warehouse-industrial-logistics-companies-commercial-huge-distribution-high-shelves-bottom-view-191288522.jpg"
    },
    {
      title: "Dynamic Allocation of Incoming Cartons",
      description: "Classifies cartons and optimizes storage allocation based on demand forecasts and warehouse capacity.",
      icon: <Shield className="w-6 h-6 text-green-600" />,
      link: "/features/security",
      imageUrl: "https://golocad.com/wp-content/uploads/2022/12/carton.webp"
    },
    {
      title: "Inventory Movement Recommendations:",
      description: "Advanced analytics and insights to make data-driven inventory decisions.",
      icon: <Database className="w-6 h-6 text-purple-600" />,
      link: "/features/analytics",
      imageUrl: "https://www.ascm.org/globalassets/ascm_website_assets/img/landing/im-01.jpg"
    },
    {
      title: "AI-Powered Warehouse Layout Optimization",
      description: "Seamless cloud integration for accessing your inventory from anywhere.",
      icon: <Cloud className="w-6 h-6 text-orange-600" />,
      link: "/features/cloud",
      imageUrl: "https://www.parcelandpostaltechnologyinternational.com/wp-content/uploads/2024/03/Parcel-hero-courier-scaled-e1710254637620-768x432.jpg"
    },
    {
      title: "Cost-Effective Parcel & Transportation Delivery",
      description: "Automate routine tasks and streamline your inventory management workflow.",
      icon: <Zap className="w-6 h-6 text-yellow-600" />,
      link: "/features/automation",
      imageUrl: "https://images.squarespace-cdn.com/content/v1/61f92d97a17c5428e2a2caa7/46492d55-f25b-40cb-8712-a03a542dddea/receiving+parcel.jpg"
    },
    {
      title: "GenAI for Smart Recommendations",
      description: "Intelligent stock level monitoring and automated reordering system.",
      icon: <BoxesIcon className="w-6 h-6 text-pink-600" />,
      link: "/features/stock",
      imageUrl: "https://partnershiponai.org/wp-content/uploads/2021/01/Recommender-Algorithms-Blog-Post_03_011821.png"
    }
  ];

  return (
    <div className="min-h-screen bg-white font-poppins">
      <Navbar />
      
      <main className="relative pt-48 pb-16 overflow-hidden">
        {/* Grid Background */}
        <div className="absolute top-0 left-0 right-0 h-[400px] z-0">
          <GridBackground />
          <div className="absolute inset-0 bg-white/30 backdrop-blur-sm" />
        </div>

        {/* Floating Icons in a Single Horizontal Line */}
        <div className="flex justify-center items-center space-x-8 absolute top-24 left-0 right-0 z-10">
          {/* Logistics */}
          <motion.div 
            className="flex flex-col items-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <motion.div
              className="bg-white/80 backdrop-blur-sm p-4 rounded-xl shadow-lg"
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 3, repeat: Infinity, ease: "easeInOut", delay: 0.2 }}
            >
              <Truck className="w-8 h-8 text-blue-600" />
            </motion.div>
            <span className="text-sm text-gray-600 mt-2 font-ibm-plex">Logistics</span>
          </motion.div>

          {/* Inventory */}
          <motion.div 
            className="flex flex-col items-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <motion.div
              className="bg-white/80 backdrop-blur-sm p-4 rounded-xl shadow-lg"
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 3, repeat: Infinity, ease: "easeInOut", delay: 0.4 }}
            >
              <BoxesIcon className="w-8 h-8 text-purple-600" />
            </motion.div>
            <span className="text-sm text-gray-600 mt-2 font-ibm-plex">Inventory</span>
          </motion.div>

          {/* Production */}
          <motion.div 
            className="flex flex-col items-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
          >
            <motion.div
              className="bg-white/80 backdrop-blur-sm p-4 rounded-xl shadow-lg"
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 3, repeat: Infinity, ease: "easeInOut", delay: 0.6 }}
            >
              <Factory className="w-8 h-8 text-green-600" />
            </motion.div>
            <span className="text-sm text-gray-600 mt-2 font-ibm-plex">Production</span>
          </motion.div>

          {/* Global */}
          <motion.div 
            className="flex flex-col items-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
          >
            <motion.div
              className="bg-white/80 backdrop-blur-sm p-4 rounded-xl shadow-lg"
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 3, repeat: Infinity, ease: "easeInOut", delay: 0.8 }}
            >
              <Globe className="w-8 h-8 text-orange-600" />
            </motion.div>
            <span className="text-sm text-gray-600 mt-2 font-ibm-plex">Global</span>
          </motion.div>

          {/* Cloud */}
          <motion.div 
            className="flex flex-col items-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1 }}
          >
            <motion.div
              className="bg-white/80 backdrop-blur-sm p-4 rounded-xl shadow-lg"
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 3, repeat: Infinity, ease: "easeInOut", delay: 1 }}
            >
              <Cloud className="w-8 h-8 text-pink-600" />
            </motion.div>
            <span className="text-sm text-gray-600 mt-2 font-ibm-plex">Cloud</span>
          </motion.div>

          {/* Security */}
          <motion.div 
            className="flex flex-col items-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.2 }}
          >
            <motion.div
              className="bg-white/80 backdrop-blur-sm p-4 rounded-xl shadow-lg"
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 3, repeat: Infinity, ease: "easeInOut", delay: 1.2 }}
            >
              <Shield className="w-8 h-8 text-teal-600" />
            </motion.div>
            <span className="text-sm text-gray-600 mt-2 font-ibm-plex">Security</span>
          </motion.div>

          {/* Efficiency */}
          <motion.div 
            className="flex flex-col items-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.4 }}
          >
            <motion.div
              className="bg-white/80 backdrop-blur-sm p-4 rounded-xl shadow-lg"
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 3, repeat: Infinity, ease: "easeInOut", delay: 1.4 }}
            >
              <Zap className="w-8 h-8 text-yellow-600" />
            </motion.div>
            <span className="text-sm text-gray-600 mt-2 font-ibm-plex">Efficiency</span>
          </motion.div>

          {/* Data */}
          <motion.div 
            className="flex flex-col items-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.6 }}
          >
            <motion.div
              className="bg-white/80 backdrop-blur-sm p-4 rounded-xl shadow-lg"
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 3, repeat: Infinity, ease: "easeInOut", delay: 1.6 }}
            >
              <Database className="w-8 h-8 text-indigo-600" />
            </motion.div>
            <span className="text-sm text-gray-600 mt-2 font-ibm-plex">Data</span>
          </motion.div>
        </div>

        {/* Main Content */}
        <div className="text-center max-w-4xl mx-auto mt-64 relative z-20">
          <h1 className="text-3xl md:text-6xl font-bold text-gray-900 mb-6 font-ibm-plex tracking-wider">
            <BlurText 
              text="Optimize • Track • Manage with InvenX"
              delay={150}
              direction="top"
            />
          </h1>
          
          <p className="text-xl text-gray-600 mb-8 font-ibm-plex">
            Transform your inventory management with cutting-edge AI technology.
            Streamline operations, reduce costs, and boost efficiency.
          </p>
          
          <motion.button
            className="bg-black text-white text-lg px-8 py-4 rounded-lg shadow-lg hover:bg-gray-900 transition-colors font-ibm-plex flex items-center justify-center space-x-2 mx-auto"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <span>Get Started</span>
            <Send className="w-5 h-5" />
          </motion.button>
        </div>
      </main>

      {/* Feature Cards Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <FeatureCard
              key={index}
              {...feature}
            />
          ))}
        </div>
      </section>
    </div>
  );
}