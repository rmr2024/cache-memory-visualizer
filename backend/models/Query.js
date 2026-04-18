import mongoose from 'mongoose';

const querySchema = new mongoose.Schema({
  question: {
    type: String,
    required: true,
    trim: true
  },
  answer: {
    type: String,
    required: true
  }
}, {
  timestamps: true
});

const Query = mongoose.model('Query', querySchema);

export default Query;