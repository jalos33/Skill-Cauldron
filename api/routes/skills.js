const express = require("express");
const router = express.Router();

// Get all skills
router.get("/skills", (req, res) => {
  res.json({ skills: [] });
});

// Get a specific skill by ID
router.get("/skills/:id", (req, res) => {
  const skillId = req.params.id;
  res.json({ skill: skillId });
});

// Create a new skill
router.post("/skills", (req, res) => {
  const newSkill = req.body;
  res.status(201).json({ created: true, skill: newSkill });
});

module.exports = router;
