import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Upload, Download, Sparkles, ArrowRight, User, Building, Briefcase } from 'lucide-react'
import CompanySelector from './CompanySelector'

function App() {
  const [companies, setCompanies] = useState([])
  const [formData, setFormData] = useState({
    name: '',
    former_company: '',
    new_company: '',
    role: '',
    announcement_text: 'MIGRATED',
    custom_announcement: '',
    profile_image: null
  })
  const [preview, setPreview] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [generatedImage, setGeneratedImage] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchCompanies()
  }, [])

  const fetchCompanies = async () => {
    try {
      const response = await axios.get('/api/companies')
      setCompanies(response.data.companies)
    } catch (err) {
      console.error('Error fetching companies:', err)
      setError('Failed to load companies')
    }
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleImageUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      setFormData(prev => ({
        ...prev,
        profile_image: file
      }))
      
      // Create preview
      const reader = new FileReader()
      reader.onload = (e) => {
        setPreview(e.target.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      const formDataToSend = new FormData()
      formDataToSend.append('name', formData.name)
      formDataToSend.append('former_company', formData.former_company)
      formDataToSend.append('new_company', formData.new_company)
      formDataToSend.append('role', formData.role)
      
      // Use custom announcement if selected, otherwise use predefined text
      const announcementText = formData.announcement_text === 'CUSTOM' 
        ? formData.custom_announcement 
        : formData.announcement_text
      formDataToSend.append('announcement_text', announcementText)
      
      formDataToSend.append('date', new Date().toISOString().split('T')[0]) // Auto-generate current date
      formDataToSend.append('profile_image', formData.profile_image)

      const response = await axios.post('/api/generate-flyer', formDataToSend, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      setGeneratedImage(response.data)
    } catch (err) {
      console.error('Error generating flyer:', err)
      setError(err.response?.data?.error || 'Failed to generate flyer')
    } finally {
      setIsLoading(false)
    }
  }

  const downloadImage = () => {
    if (generatedImage) {
      const link = document.createElement('a')
      link.href = `data:image/png;base64,${generatedImage.image_data}`
      link.download = generatedImage.filename
      link.click()
    }
  }

  const resetForm = () => {
    setFormData({
      name: '',
      former_company: '',
      new_company: '',
      role: '',
      announcement_text: 'MIGRATED',
      custom_announcement: '',
      profile_image: null
    })
    setPreview(null)
    setGeneratedImage(null)
    setError('')
  }

  return (
    <div className="min-h-screen p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center items-center gap-2 mb-4">
            <Sparkles className="w-8 h-8 text-yellow-400" />
            <h1 className="text-4xl md:text-5xl font-bold text-white">
            Tech Trades
            </h1>
            <Sparkles className="w-8 h-8 text-yellow-400" />
          </div>
          <p className="text-xl text-white/80 max-w-2xl mx-auto">
            Create professional flyers to announce your career moves to the tech community
          </p>
        </div>

        {/* Main Content */}
        <div className="grid md:grid-cols-2 gap-8">
          {/* Form Section */}
          <div className="glass-card p-6 md:p-8">
            <h2 className="text-2xl font-semibold text-white mb-6 flex items-center gap-2">
              <User className="w-6 h-6" />
              Create Your Announcement
            </h2>

            {error && (
              <div className="bg-red-500/20 border border-red-500/50 text-red-100 px-4 py-3 rounded-lg mb-6">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Name */}
              <div>
                <label className="block text-white font-medium mb-2">
                  <User className="w-4 h-4 inline mr-2" />
                  Full Name
                </label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  className="input-field"
                  placeholder="Enter your full name"
                  required
                />
              </div>

              {/* Former Company */}
              <div>
                <label className="block text-white font-medium mb-2">
                  <Building className="w-4 h-4 inline mr-2" />
                  Former Company
                </label>
                <CompanySelector
                  companies={companies}
                  value={formData.former_company}
                  onChange={handleInputChange}
                  placeholder="Select your former company"
                  name="former_company"
                />
                <p className="text-xs text-white/60 mt-1">Can't find your company? Use "Add Custom Company" at the bottom of the list.</p>
              </div>

              {/* New Company */}
              <div>
                <label className="block text-white font-medium mb-2">
                  <Building className="w-4 h-4 inline mr-2" />
                  New Company
                </label>
                <CompanySelector
                  companies={companies}
                  value={formData.new_company}
                  onChange={handleInputChange}
                  placeholder="Select your new company"
                  name="new_company"
                />
                <p className="text-xs text-white/60 mt-1">Can't find your company? Use "Add Custom Company" at the bottom of the list.</p>
              </div>

              {/* Role */}
              <div>
                <label className="block text-white font-medium mb-2">
                  <Briefcase className="w-4 h-4 inline mr-2" />
                  Role
                </label>
                <input
                  type="text"
                  name="role"
                  value={formData.role}
                  onChange={handleInputChange}
                  className="input-field"
                  placeholder="e.g., Senior Software Engineer"
                  required
                />
              </div>

              {/* Announcement Text */}
              <div>
                <label className="block text-white font-medium mb-2">
                  <Sparkles className="w-4 h-4 inline mr-2" />
                  Announcement Text
                </label>
                <div className="space-y-2">
                  <select
                    name="announcement_text"
                    value={formData.announcement_text}
                    onChange={handleInputChange}
                    className="input-field"
                    required
                  >
                    <option value="MIGRATED">MIGRATED</option>
                    <option value="SIGNED">SIGNED</option>
                    <option value="TRANSFER COMPLETE">TRANSFER COMPLETE</option>
                    <option value="TECH DEAL SEALED">TECH DEAL SEALED</option>
                    <option value="BIG MOVE">BIG MOVE</option>
                    <option value="CUSTOM">Enter Your Own</option>
                  </select>
                  
                  {formData.announcement_text === 'CUSTOM' && (
                    <input
                      type="text"
                      name="custom_announcement"
                      value={formData.custom_announcement || ''}
                      onChange={(e) => setFormData({...formData, custom_announcement: e.target.value})}
                      className="input-field"
                      placeholder="Enter your custom announcement text"
                      required
                    />
                  )}
                </div>
                <p className="text-xs text-white/60 mt-1">Choose a predefined announcement or enter your own text.</p>
              </div>

              {/* Profile Image */}
              <div>
                <label className="block text-white font-medium mb-2">
                  <Upload className="w-4 h-4 inline mr-2" />
                  Profile Picture
                </label>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageUpload}
                  className="input-field"
                  required
                />
                {preview && (
                  <div className="mt-4 flex justify-center">
                    <img
                      src={preview}
                      alt="Preview"
                      className="w-32 h-32 object-cover rounded-full border-4 border-white/30"
                    />
                  </div>
                )}
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={isLoading}
                className="btn-primary w-full flex items-center justify-center gap-2"
              >
                {isLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    Generating...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    Generate Flyer
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Preview Section */}
          <div className="glass-card p-6 md:p-8">
            <h2 className="text-2xl font-semibold text-white mb-6 flex items-center gap-2">
              <Download className="w-6 h-6" />
              Your Flyer
            </h2>

            {generatedImage ? (
              <div className="space-y-4">
                <div className="bg-white/10 rounded-lg p-4">
                  <img
                    src={`data:image/png;base64,${generatedImage.image_data}`}
                    alt="Generated flyer"
                    className="w-full h-auto rounded-lg shadow-lg"
                  />
                </div>
                <div className="flex gap-3">
                  <button
                    onClick={downloadImage}
                    className="btn-primary flex items-center gap-2 flex-1"
                  >
                    <Download className="w-4 h-4" />
                    Download
                  </button>
                  <button
                    onClick={resetForm}
                    className="btn-secondary flex items-center gap-2"
                  >
                    Create Another
                  </button>
                </div>
              </div>
            ) : (
              <div className="bg-white/5 border-2 border-dashed border-white/30 rounded-lg p-8 text-center">
                <div className="text-white/60 mb-4">
                  <Sparkles className="w-16 h-16 mx-auto mb-4" />
                  <p className="text-lg">Your flyer will appear here</p>
                  <p className="text-sm mt-2">Fill out the form to generate your tech transfer announcement</p>
                </div>
                
                {/* Preview of what it will look like */}
                {formData.name && formData.former_company && formData.new_company && (
                  <div className="bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg p-4 text-white text-center mt-6">
                    <p className="text-sm opacity-80">Preview:</p>
                    <div className="flex items-center justify-center gap-2 mt-2">
                      <div className="flex items-center gap-1">
                        {companies.find(c => c.name === formData.former_company) ? (
                          <img
                            src={companies.find(c => c.name === formData.former_company)?.logo}
                            alt={formData.former_company}
                            className="w-8 h-8 object-contain"
                            onError={(e) => { e.target.style.display = 'none' }}
                          />
                        ) : (
                          <div className="w-8 h-8 bg-white/30 rounded flex items-center justify-center">
                            <span className="text-xs">?</span>
                          </div>
                        )}
                        <span className="lilita-one-regular text-sm">{formData.former_company}</span>
                      </div>
                      <ArrowRight className="w-4 h-4 text-black" />
                      <div className="flex items-center gap-1">
                        {companies.find(c => c.name === formData.new_company) ? (
                          <img
                            src={companies.find(c => c.name === formData.new_company)?.logo}
                            alt={formData.new_company}
                            className="w-8 h-8  object-contain"
                            onError={(e) => { e.target.style.display = 'none' }}
                          />
                        ) : (
                          <div className="w-8 h-8  bg-white/30 rounded flex items-center justify-center">
                            <span className="text-xs">?</span>
                          </div>
                        )}
                        <span className="lilita-one-regular text-sm">{formData.new_company}</span>
                      </div>
                    </div>
                    <p className="spicy-rice-regular font-bold mt-2 text-3xl">{formData.name.toUpperCase()}</p>
                    <p className="lilita-one-regular text-sm mt-1 font-bold">
                      {formData.announcement_text === 'CUSTOM' 
                        ? formData.custom_announcement.toUpperCase() 
                        : formData.announcement_text}
                    </p>
                    {formData.role && (
                      <p className="lilita-one-regular text-xl mt-1 font-bold">{formData.role.toUpperCase()}</p>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App 