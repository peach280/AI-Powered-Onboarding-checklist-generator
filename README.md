---
title: berry-backend
emoji: 🧠
colorFrom: indigo
colorTo: pink
sdk: docker
pinned: false
---

# AI-Powered Onboarding Checklist Generator

A full-stack web application that takes a documentation URL and uses the Google Gemini API to automatically generate a structured, interactive onboarding checklist for new users.

<video controls src="demo.mp4" title="Title"></video>

---

## Features

* **Dynamic Checklist Generation:** Enter any public documentation URL to get a custom checklist.
* **Real-time Web Scraping:** Fetches and parses content from the provided URL on the fly.
* **High-Quality AI:** Leverages the power of the Google Gemini API (`gemini-1.5-flash`) for accurate and relevant content generation.
* **Interactive UI:** A clean, modern frontend built with `React` where users can check off items.
* **Full-Stack Architecture:** Demonstrates a complete pipeline from a frontend client to a backend server and a third-party AI service.

---

## Tech Stack

* **Frontend:** `React`, `CSS`
* **Backend:** `Python`, `Flask`
* **AI Service:** Google Gemini API
* **Web Scraping:** `requests`, `BeautifulSoup`
* **Deployment:**
    * Frontend deployed on **Vercel**.
    * Backend deployed on **Hugging Face Spaces**.

