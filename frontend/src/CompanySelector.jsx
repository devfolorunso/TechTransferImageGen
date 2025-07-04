import React, { useState, useRef, useEffect } from 'react'
import { ChevronDown, Search } from 'lucide-react'

const CompanySelector = ({ companies, value, onChange, placeholder, name }) => {
  const [isOpen, setIsOpen] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [showCustomInput, setShowCustomInput] = useState(false)
  const [customCompanyName, setCustomCompanyName] = useState('')
  const dropdownRef = useRef(null)

  const filteredCompanies = companies.filter(company =>
    company.name.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const selectedCompany = companies.find(c => c.name === value)
  const isCustomCompany = value && !selectedCompany

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false)
        setShowCustomInput(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  // Update custom company name when value changes
  useEffect(() => {
    if (isCustomCompany) {
      setCustomCompanyName(value)
    }
  }, [value, isCustomCompany])

  const handleSelect = (company) => {
    onChange({ target: { name, value: company.name } })
    setIsOpen(false)
    setSearchTerm('')
    setShowCustomInput(false)
  }

  const handleCustomSelect = () => {
    setShowCustomInput(true)
    setIsOpen(false)
    setSearchTerm('')
  }

  const handleCustomSubmit = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (customCompanyName.trim()) {
      onChange({ target: { name, value: customCompanyName.trim() } })
      setShowCustomInput(false)
      setCustomCompanyName('')
    }
  }

  const handleCustomChange = (e) => {
    const newValue = e.target.value
    setCustomCompanyName(newValue)
    // Don't trigger onChange until user submits
  }

  return (
    <div className="relative" ref={dropdownRef}>
      {/* Custom Company Input */}
      {showCustomInput ? (
        <div className="relative">
          <div className="space-y-2">
            <input
              type="text"
              value={customCompanyName}
              onChange={handleCustomChange}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault()
                  handleCustomSubmit(e)
                }
                if (e.key === 'Escape') {
                  setShowCustomInput(false)
                  setCustomCompanyName('')
                }
              }}
              placeholder="Enter your company name"
              className="input-field"
              autoFocus
            />
            <div className="flex gap-2">
              <button
                type="button"
                onClick={handleCustomSubmit}
                className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 transition-colors disabled:opacity-50"
                disabled={!customCompanyName.trim()}
              >
                Add Company
              </button>
              <button
                type="button"
                onClick={(e) => {
                  e.preventDefault()
                  e.stopPropagation()
                  setShowCustomInput(false)
                  setCustomCompanyName('')
                }}
                className="bg-gray-300 text-gray-700 px-3 py-1 rounded text-sm hover:bg-gray-400 transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      ) : (
        <>
          {/* Trigger Button */}
          <button
            type="button"
            onClick={() => setIsOpen(!isOpen)}
            className="input-field flex items-center justify-between w-full text-left"
          >
            <div className="flex items-center gap-2">
              {selectedCompany ? (
                <>
                  <img
                    src={selectedCompany.logo}
                    alt={selectedCompany.name}
                    className="w-5 h-5 object-contain"
                    onError={(e) => { e.target.style.display = 'none' }}
                  />
                  <span className="text-gray-900">{selectedCompany.name}</span>
                </>
              ) : isCustomCompany ? (
                <>
                  <div className="w-5 h-5 bg-gray-300 rounded flex items-center justify-center">
                    <span className="text-xs text-gray-600">?</span>
                  </div>
                  <span className="text-gray-900">{value}</span>
                </>
              ) : (
                <span className="text-gray-500">{placeholder}</span>
              )}
            </div>
            <ChevronDown className={`w-4 h-4 text-gray-500 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
          </button>
        </>
      )}

      {/* Dropdown */}
      {isOpen && !showCustomInput && (
        <div className="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-80 overflow-hidden">
          {/* Search Input */}
          <div className="p-3 border-b border-gray-200">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search companies..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* Options List */}
          <div className="max-h-60 overflow-y-auto">
            {filteredCompanies.length > 0 ? (
              <>
                {filteredCompanies.map((company) => (
                  <button
                    key={company.name}
                    type="button"
                    onClick={() => handleSelect(company)}
                    className="w-full px-4 py-3 flex items-center gap-3 hover:bg-gray-50 transition-colors text-left"
                  >
                    <img
                      src={company.logo}
                      alt={company.name}
                      className="w-6 h-6 object-contain flex-shrink-0"
                      onError={(e) => { e.target.style.display = 'none' }}
                    />
                    <span className="text-gray-900 font-medium">{company.name}</span>
                  </button>
                ))}
                {/* Add Custom Company Option */}
                <div className="border-t border-gray-200 mt-1 pt-1">
                  <button
                    type="button"
                    onClick={handleCustomSelect}
                    className="w-full px-4 py-3 flex items-center gap-3 hover:bg-blue-50 transition-colors text-left text-blue-600"
                  >
                    <div className="w-6 h-6 bg-blue-100 rounded flex items-center justify-center flex-shrink-0">
                      <span className="text-blue-600 font-bold text-sm">+</span>
                    </div>
                    <span className="font-medium">Add Custom Company</span>
                  </button>
                </div>
              </>
            ) : (
              <>
                <div className="px-4 py-3 text-gray-500 text-center">
                  No companies found
                </div>
                {/* Add Custom Company Option when search has no results */}
                <div className="border-t border-gray-200 mt-1 pt-1">
                  <button
                    type="button"
                    onClick={handleCustomSelect}
                    className="w-full px-4 py-3 flex items-center gap-3 hover:bg-blue-50 transition-colors text-left text-blue-600"
                  >
                    <div className="w-6 h-6 bg-blue-100 rounded flex items-center justify-center flex-shrink-0">
                      <span className="text-blue-600 font-bold text-sm">+</span>
                    </div>
                    <span className="font-medium">Add Custom Company</span>
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default CompanySelector 