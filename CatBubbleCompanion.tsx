import { useEffect, useState, useRef } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { useTheme } from "../../context/ThemeContext"
import ThemeToggle from "./ThemeToggle"
import LanguageToggle from "./LanguageToggle"
import {
  type HeartParticle,
  playCatSound,
  createBurstHearts,
} from "../../utils/catEffects"

export default function CatBubbleCompanion() {
  const { isLight } = useTheme()
  const [activeState, setActiveState] = useState<"idle" | "moving" | "clicking" | "hovering" | "scrolling" | "waiting">("idle")

  // Event tracking states
  const [isClicking, setIsClicking] = useState(false)
  const [isHovering, setIsHovering] = useState(false)
  const [isScrolling, setIsScrolling] = useState(false)
  const [isMoving, setIsMoving] = useState(false)
  const [isLoading, setIsLoading] = useState(true) // Start true to trigger waiting spin on load
  const [isVisible, setIsVisible] = useState(true)  // Tracks visibility based on idle time
  const [frame, setFrame] = useState(0)
  const [showMobileControls, setShowMobileControls] = useState(false)
  const companionRef = useRef<HTMLDivElement | null>(null)

  const [hearts, setHearts] = useState<HeartParticle[]>([])
  const nextHeartId = useRef(0)
  const lastMeowTimeRef = useRef(0)
  const [isMouthMoving, setIsMouthMoving] = useState(false)
  const mouthTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  const scrollTimeout = useRef<ReturnType<typeof setTimeout> | null>(null)
  const moveTimeout = useRef<ReturnType<typeof setTimeout> | null>(null)
  const lastMousePos = useRef({ x: 0, y: 0 })
  const lastActivityTime = useRef(Date.now())

  const playMeow = () => {
    playCatSound("/sounds/meow.wav", 1.0 + (Math.random() - 0.5) * 0.15, 0.55)
    setIsMouthMoving(true)
    if (mouthTimeoutRef.current) clearTimeout(mouthTimeoutRef.current)
    mouthTimeoutRef.current = setTimeout(() => {
      setIsMouthMoving(false)
    }, 450)
  }

  // Reset idle timer upon any user interaction
  const resetIdleTimer = () => {
    lastActivityTime.current = Date.now()
  }

  // Animation frame counter — only runs when companion is visible
  useEffect(() => {
    if (!isVisible) return

    const interval = setInterval(() => {
      setFrame((f) => (f + 1) % 100)
    }, 200)
    return () => clearInterval(interval)
  }, [isVisible])

  // Idle detection — runs at a slower cadence (500ms is plenty for "idle for 4s?" check)
  useEffect(() => {
    const idleCheck = setInterval(() => {
      const idleTime = Date.now() - lastActivityTime.current
      const shouldBeVisible = isLoading || isHovering || showMobileControls || (idleTime < 4000)
      setIsVisible(shouldBeVisible)
    }, 500)
    return () => clearInterval(idleCheck)
  }, [isLoading, isHovering, showMobileControls])

  // Close mobile controls popover when clicking/touching outside companion
  useEffect(() => {
    if (!showMobileControls) return
    const handleClickOutside = (e: MouseEvent | TouchEvent) => {
      if (companionRef.current && !companionRef.current.contains(e.target as Node)) {
        setShowMobileControls(false)
      }
    }
    document.addEventListener("mousedown", handleClickOutside)
    document.addEventListener("touchstart", handleClickOutside)
    return () => {
      document.removeEventListener("mousedown", handleClickOutside)
      document.removeEventListener("touchstart", handleClickOutside)
    }
  }, [showMobileControls])

  // Detect page load state with automatic 1.5s fallback
  useEffect(() => {
    if (document.readyState === "complete") {
      setIsLoading(false)
      return
    }

    setIsLoading(true)
    const handleStopLoading = () => setIsLoading(false)
    window.addEventListener("load", handleStopLoading)

    const fallbackTimeout = setTimeout(() => {
      setIsLoading(false)
    }, 1500)

    return () => {
      window.removeEventListener("load", handleStopLoading)
      clearTimeout(fallbackTimeout)
    }
  }, [])

  // Global event listeners to drive companion animations
  useEffect(() => {
    let mouseRafId: number | null = null

    const handleWindowMouseMove = (e: MouseEvent) => {
      resetIdleTimer()
      if (mouseRafId !== null) return

      mouseRafId = requestAnimationFrame(() => {
        mouseRafId = null
        const dx = Math.abs(e.clientX - lastMousePos.current.x)
        const dy = Math.abs(e.clientY - lastMousePos.current.y)
        
        // Significant movement triggers walking state
        if (dx > 4 || dy > 4) {
          setIsMoving(true)
          if (moveTimeout.current) clearTimeout(moveTimeout.current)
          moveTimeout.current = setTimeout(() => setIsMoving(false), 300)
        }
        lastMousePos.current = { x: e.clientX, y: e.clientY }
      })
    }

    const handleWindowTouchMove = () => {
      resetIdleTimer()
      // Finger drag acts as movement in mobile
      setIsMoving(true)
      if (moveTimeout.current) clearTimeout(moveTimeout.current)
      moveTimeout.current = setTimeout(() => setIsMoving(false), 350)
    }

    const handleMouseDown = () => {
      resetIdleTimer()
      setIsClicking(true)
    }
    const handleMouseUp = () => {
      resetIdleTimer()
      setIsClicking(false)
    }
    
    const handleTouchStart = () => {
      resetIdleTimer()
      setIsClicking(true)
    }
    const handleTouchEnd = () => {
      resetIdleTimer()
      setIsClicking(false)
    }

    const handleScroll = () => {
      resetIdleTimer()
      setIsScrolling(true)
      if (scrollTimeout.current) clearTimeout(scrollTimeout.current)
      scrollTimeout.current = setTimeout(() => setIsScrolling(false), 300)
    }

    window.addEventListener("mousemove", handleWindowMouseMove)
    window.addEventListener("mousedown", handleMouseDown)
    window.addEventListener("mouseup", handleMouseUp)
    window.addEventListener("scroll", handleScroll, { passive: true })

    window.addEventListener("touchstart", handleTouchStart, { passive: true })
    window.addEventListener("touchmove", handleWindowTouchMove, { passive: true })
    window.addEventListener("touchend", handleTouchEnd)

    return () => {
      window.removeEventListener("mousemove", handleWindowMouseMove)
      window.removeEventListener("mousedown", handleMouseDown)
      window.removeEventListener("mouseup", handleMouseUp)
      window.removeEventListener("scroll", handleScroll)

      window.removeEventListener("touchstart", handleTouchStart)
      window.removeEventListener("touchmove", handleWindowTouchMove)
      window.removeEventListener("touchend", handleTouchEnd)

      if (mouseRafId !== null) cancelAnimationFrame(mouseRafId)
      if (scrollTimeout.current) clearTimeout(scrollTimeout.current)
      if (moveTimeout.current) clearTimeout(moveTimeout.current)
      if (mouthTimeoutRef.current) clearTimeout(mouthTimeoutRef.current)
    }
  }, [])

  const handleBubbleClick = (e: React.MouseEvent<HTMLDivElement>) => {
    setShowMobileControls((prev) => !prev)

    const now = Date.now()
    if (now - lastMeowTimeRef.current < 1200) return // 1.2s cooldown to prevent spam clicking
    lastMeowTimeRef.current = now

    playMeow()

    const rect = e.currentTarget.getBoundingClientRect()
    const clickX = rect.width / 2
    const clickY = rect.height / 2

    const newHearts = createBurstHearts(nextHeartId.current, 12, clickX, clickY, {
      minDist: 30,
      maxDist: 85,
      baseScale: 0.9,
      scaleVariance: 0.6,
      rotationVariance: 60,
      offsetY: -15,
    })
    nextHeartId.current += newHearts.length

    setHearts((prev) => [...prev, ...newHearts])
    setTimeout(() => {
      setHearts((prev) => prev.filter((h) => !newHearts.some((nh) => nh.id === h.id)))
    }, 1500)
  }

  // Resolve current active animation state
  useEffect(() => {
    if (isLoading) {
      setActiveState("waiting")
    } else if (isHovering) {
      setActiveState("hovering")
    } else if (isClicking) {
      setActiveState("clicking")
    } else if (isScrolling) {
      setActiveState("scrolling")
    } else if (isMoving) {
      setActiveState("moving")
    } else {
      setActiveState("idle")
    }
  }, [isLoading, isHovering, isClicking, isScrolling, isMoving])

  // Custom styling parameters based on state & theme
  const catColor = isLight ? "#fb8c00" : "#a1a1aa" // Orange awake vs silver-gray sleeping
  const shadowColor = isLight ? "#e65100" : "#71717a" // Dark orange shadow vs dark gray shadow
  const pinkColor = "#ff8a80"    // Soft pink ears/nose
  const blackColor = isLight ? "#3e2723" : "#18181b" // Soft dark brown outline vs black outline
  const whiteColor = "#ffffff"
  const stripeColor = isLight ? "#d84315" : "#787880" // Dark reddish-orange stripes vs darker gray stripes
  const whiskerColor = isLight ? blackColor : "#ffffff"

  // 1. Head transform calculations
  let headTranslateY = 0
  let headRotate = 0
  if (activeState === "idle") {
    // Soft breathing bob (0px to -1.5px)
    headTranslateY = Math.sin(frame * 0.2) * 0.75 - 0.75
  } else if (activeState === "moving") {
    // Walking head sway
    headRotate = Math.sin(frame * 0.6) * 4
    headTranslateY = Math.abs(Math.sin(frame * 0.6)) * -2
  } else if (activeState === "clicking") {
    // Ears flatten down, head sinks
    headTranslateY = 3
  } else if (activeState === "scrolling") {
    // Climbing bob
    headTranslateY = Math.sin(frame * 0.8) * 1.5
    headRotate = Math.sin(frame * 0.8) * 6
  }

  // 2. Ear flattening style
  const leftEarRotation = activeState === "clicking" ? "rotate(-12deg) translate(-2px, 3px)" : "rotate(0deg)"
  const rightEarRotation = activeState === "clicking" ? "rotate(12deg) translate(2px, 3px)" : "rotate(0deg)"

  // 3. Winking eye scale
  const rightEyeScaleY = activeState === "hovering" ? 0.15 : 1

  // 4. Paw action styling
  let leftPawTransform = "translate(0, 0)"
  let rightPawTransform = "translate(0, 0)"
  if (activeState === "moving") {
    leftPawTransform = `translateY(${Math.sin(frame * 0.6) * 3}px)`
    rightPawTransform = `translateY(${Math.cos(frame * 0.6) * 3}px)`
  } else if (activeState === "clicking") {
    // Paws reach out/extend
    leftPawTransform = "translate(-2px, -5px) scaleY(1.2)"
    rightPawTransform = "translate(2px, -5px) scaleY(1.2)"
  } else if (activeState === "hovering") {
    // Left paw waves, right paw stays down
    leftPawTransform = `translate(-3px, -11px) rotate(${Math.sin(frame * 1.0) * 18}deg)`
  } else if (activeState === "scrolling") {
    // Rapid climbing paws
    leftPawTransform = `translateY(${Math.sin(frame * 0.9) * 4}px)`
    rightPawTransform = `translateY(${Math.cos(frame * 0.9) * 4}px)`
  }

  // 5. Tail wagging styling
  let tailRotate = 0
  if (activeState === "idle") {
    tailRotate = Math.sin(frame * 0.15) * 10
  } else if (activeState === "moving") {
    tailRotate = Math.sin(frame * 0.5) * 18
  } else if (activeState === "scrolling") {
    tailRotate = Math.sin(frame * 0.8) * 22
  } else if (activeState === "clicking") {
    tailRotate = -15
  }

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          ref={companionRef}
          initial={{ opacity: 0, scale: 0.8, y: 30 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.8, y: 30 }}
          transition={{ type: "spring", stiffness: 260, damping: 20 }}
          onMouseEnter={() => setIsHovering(true)}
          onMouseLeave={() => setIsHovering(false)}
          className="fixed bottom-20 sm:bottom-24 md:bottom-8 right-4 sm:right-6 md:right-8 z-[9999] select-none pointer-events-auto"
        >
          {/* Mobile Quick Controls Popover (Language & Theme Toggle) */}
          <AnimatePresence>
            {showMobileControls && (
              <motion.div
                initial={{ opacity: 0, scale: 0.8, y: 12 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.8, y: 12 }}
                transition={{ type: "spring", stiffness: 380, damping: 24 }}
                onClick={(e) => e.stopPropagation()}
                className="md:hidden absolute bottom-[calc(100%+14px)] right-0 z-[10000] flex items-center gap-2.5 p-2 rounded-2xl bg-white/95 dark:bg-neutral-900/95 border border-neutral-200/80 dark:border-neutral-700/60 shadow-[0_10px_30px_rgba(0,0,0,0.08)] dark:shadow-[0_10px_30px_rgba(0,0,0,0.5)] backdrop-blur-xl touch-auto pointer-events-auto"
              >
                <LanguageToggle />
                <div className="w-[1px] h-5 bg-neutral-300/80 dark:bg-neutral-700/60" />
                <ThemeToggle />
              </motion.div>
            )}
          </AnimatePresence>

          {/* Glassmorphic Bubble Outer Ring */}
          <div
            onClick={handleBubbleClick}
            className="relative w-16 h-16 sm:w-20 sm:h-20 rounded-full flex items-center justify-center cursor-pointer group border border-neutral-200/60 dark:border-neutral-800/40 backdrop-blur-md bg-white/40 dark:bg-neutral-900/40 transition-all duration-300 hover:scale-110 hover:border-neutral-400 dark:hover:border-neutral-600 animate-bubble-float"
          >
            {/* Click-to-spawn smooth drifting small hearts */}
            {hearts.map((h) => (
              <motion.span
                key={h.id}
                initial={{
                  opacity: 1,
                  scale: 0,
                  x: h.x,
                  y: h.y,
                  rotate: 0,
                }}
                animate={{
                  opacity: 0,
                  scale: h.scale,
                  x: h.x + h.targetX,
                  y: h.y + h.targetY - 35,
                  rotate: h.rotation,
                }}
                transition={{
                  duration: 1.2,
                  ease: "easeOut",
                }}
                className="absolute text-sm pointer-events-none select-none z-50 origin-center"
                style={{
                  left: 0,
                  top: 0,
                  transform: "translate(-50%, -50%)",
                }}
              >
                {h.emoji}
              </motion.span>
            ))}
            
            {/* Spinning loading wrapper */}
            <div 
              className={`w-12 h-12 sm:w-16 sm:h-16 flex items-center justify-center transition-transform duration-300 ${activeState === "waiting" ? "animate-spin" : ""}`}
            >
              
              {/* Clean Vector Cat SVG (viewBox 0 0 40 40) */}
              <svg 
                width="100%" 
                height="100%" 
                viewBox="0 0 40 40" 
                className="overflow-visible"
              >
                {/* Waving Tail (Base + Stripes + Tip) */}
                <g
                  className="transition-transform duration-150 origin-[13px_28px]"
                  style={{ transform: `rotate(${tailRotate}deg)` }}
                >
                  {/* Tail Base */}
                  <path
                    d="M 12,28 C 10,24 8,20 12,14 C 13,12 15,13 14,16 C 12,20 13,22 15,28 Z"
                    fill={catColor}
                  />
                  {/* Tail Tip */}
                  <path
                    d="M 12,14 C 13,12 15,13 14,16 C 13,15.5 12,14.5 12,14 Z"
                    fill={stripeColor}
                  />
                  {/* Tail Stripes */}
                  <path d="M 9.5,23 C 10.5,22.5 11.5,22.8 12.5,23.5" fill="none" stroke={stripeColor} strokeWidth="0.8" strokeLinecap="round" />
                  <path d="M 10,19 C 11,18.5 12,18.8 13,19.5" fill="none" stroke={stripeColor} strokeWidth="0.8" strokeLinecap="round" />
                </g>

                {/* Body Base */}
                <ellipse 
                  cx="20" 
                  cy="27" 
                  rx="10" 
                  ry="8" 
                  fill={catColor} 
                />

                {/* Body Stripes (Left and Right) */}
                <path d="M 10.5,25 Q 13,25.5 14,26.5" fill="none" stroke={stripeColor} strokeWidth="1.0" strokeLinecap="round" />
                <path d="M 10.2,28 Q 12.5,28.5 13.5,29.5" fill="none" stroke={stripeColor} strokeWidth="1.0" strokeLinecap="round" />
                <path d="M 29.5,25 Q 27,25.5 26,26.5" fill="none" stroke={stripeColor} strokeWidth="1.0" strokeLinecap="round" />
                <path d="M 29.8,28 Q 27.5,28.5 26.5,29.5" fill="none" stroke={stripeColor} strokeWidth="1.0" strokeLinecap="round" />
                
                {/* White Chest Patch */}
                <ellipse 
                  cx="20" 
                  cy="28" 
                  rx="6" 
                  ry="4.5" 
                  fill={whiteColor} 
                />

                {/* Back Foot (Cute sitting circle) */}
                {activeState === "idle" && (
                  <circle 
                    cx="10" 
                    cy="31" 
                    r="3" 
                    fill={shadowColor} 
                  />
                )}

                {/* Head Wrapper (With state-driven transitions) */}
                <g 
                  className="transition-transform duration-150 origin-[20px_20px]"
                  style={{ transform: `translateY(${headTranslateY}px) rotate(${headRotate}deg)` }}
                >
                  {/* Left Ear */}
                  <g style={{ transform: leftEarRotation }} className="transition-transform duration-150 origin-[12px_14px]">
                    <path d="M 8,14 L 5,3 L 15,10 Z" fill={catColor} />
                    <path d="M 9,13 L 7,5 L 13,10 Z" fill={pinkColor} />
                  </g>

                  {/* Right Ear */}
                  <g style={{ transform: rightEarRotation }} className="transition-transform duration-150 origin-[28px_14px]">
                    <path d="M 32,14 L 35,3 L 25,10 Z" fill={catColor} />
                    <path d="M 31,13 L 33,5 L 27,10 Z" fill={pinkColor} />
                  </g>

                  {/* Head Face Base */}
                  <ellipse cx="20" cy="18" rx="12.5" ry="10" fill={catColor} />

                  {/* Forehead Tabby M Marking */}
                  <path 
                    d="M 17.5,9.5 Q 19,13 20,13 Q 21,13 22.5,9.5 M 20,9.5 L 20,12" 
                    fill="none" 
                    stroke={stripeColor} 
                    strokeWidth="0.9" 
                    strokeLinecap="round" 
                  />

                  {/* Cheek Tabby Stripes */}
                  {/* Left Cheek Stripes */}
                  <path d="M 8.5,17 Q 11,18 12,18" fill="none" stroke={stripeColor} strokeWidth="0.8" strokeLinecap="round" />
                  <path d="M 8,19 Q 10.5,19.5 11.5,19.5" fill="none" stroke={stripeColor} strokeWidth="0.8" strokeLinecap="round" />
                  {/* Right Cheek Stripes */}
                  <path d="M 31.5,17 Q 29,18 28,18" fill="none" stroke={stripeColor} strokeWidth="0.8" strokeLinecap="round" />
                  <path d="M 32,19 Q 29.5,19.5 28.5,19.5" fill="none" stroke={stripeColor} strokeWidth="0.8" strokeLinecap="round" />

                  {/* Cheek highlights */}
                  <ellipse cx="10" cy="20" rx="2" ry="1.2" fill={pinkColor} opacity="0.6" />
                  <ellipse cx="30" cy="20" rx="2" ry="1.2" fill={pinkColor} opacity="0.6" />

                  {/* Whiskers */}
                  {/* Left Whiskers */}
                  <line x1="10" y1="21.5" x2="4" y2="21.2" stroke={whiskerColor} strokeWidth="0.5" strokeLinecap="round" opacity={isLight ? "0.3" : "0.45"} />
                  <line x1="10" y1="22.5" x2="3.5" y2="23.2" stroke={whiskerColor} strokeWidth="0.5" strokeLinecap="round" opacity={isLight ? "0.3" : "0.45"} />
                  {/* Right Whiskers */}
                  <line x1="30" y1="21.5" x2="36" y2="21.2" stroke={whiskerColor} strokeWidth="0.5" strokeLinecap="round" opacity={isLight ? "0.3" : "0.45"} />
                  <line x1="30" y1="22.5" x2="36.5" y2="23.2" stroke={whiskerColor} strokeWidth="0.5" strokeLinecap="round" opacity={isLight ? "0.3" : "0.45"} />

                  {/* Left Eye */}
                  <circle cx="15" cy="18" r="2.0" fill={blackColor} />
                  <circle cx="14.3" cy="17.3" r="0.6" fill={whiteColor} />

                  {/* Right Eye (Can wink on hover) */}
                  <ellipse 
                    cx="25" 
                    cy="18" 
                    rx="2.0" 
                    ry={`${2.0 * rightEyeScaleY}`} 
                    fill={blackColor} 
                    className="transition-all duration-150 origin-[25px_18px]"
                  />
                  {activeState !== "hovering" && (
                    <circle cx="24.3" cy="17.3" r="0.6" fill={whiteColor} />
                  )}

                  {/* Nose */}
                  <polygon points="20,20.2 18.8,21.5 21.2,21.5" fill={pinkColor} />

                  {/* Kitty Mouth (w smile or open oval when meowing) */}
                  {isMouthMoving ? (
                    <ellipse 
                      cx="20" 
                      cy="24.2" 
                      rx="1.8" 
                      ry="2.2" 
                      fill={pinkColor} 
                      stroke={blackColor} 
                      strokeWidth="0.8" 
                    />
                  ) : (
                    <path 
                      d="M 17.5,23 Q 18.8,24.2 20,23 Q 21.2,24.2 22.5,23" 
                      fill="none" 
                      stroke={blackColor} 
                      strokeWidth="1.0" 
                      strokeLinecap="round" 
                    />
                  )}
                </g>

                {/* Left Paw (Hand) */}
                <g 
                  className="transition-transform duration-150 origin-[14px_32px]"
                  style={{ transform: leftPawTransform }}
                >
                  <ellipse 
                    cx="14" 
                    cy="32" 
                    rx="3.5" 
                    ry="2.2" 
                    fill={activeState === "hovering" ? catColor : shadowColor} 
                  />
                  {/* Toe Lines */}
                  <line x1="13" y1="31" x2="13" y2="33" stroke={stripeColor} strokeWidth="0.6" strokeLinecap="round" opacity="0.6" />
                  <line x1="15" y1="31" x2="15" y2="33" stroke={stripeColor} strokeWidth="0.6" strokeLinecap="round" opacity="0.6" />
                </g>
                
                {/* Right Paw (Hand) */}
                <g 
                  className="transition-transform duration-150 origin-[26px_32px]"
                  style={{ transform: rightPawTransform }}
                >
                  <ellipse 
                    cx="26" 
                    cy="32" 
                    rx="3.5" 
                    ry="2.2" 
                    fill={shadowColor} 
                  />
                  {/* Toe Lines */}
                  <line x1="25" y1="31" x2="25" y2="33" stroke={stripeColor} strokeWidth="0.6" strokeLinecap="round" opacity="0.6" />
                  <line x1="27" y1="31" x2="27" y2="33" stroke={stripeColor} strokeWidth="0.6" strokeLinecap="round" opacity="0.6" />
                </g>
              </svg>

            </div>

          </div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
